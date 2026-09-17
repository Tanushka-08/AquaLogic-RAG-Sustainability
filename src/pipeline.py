"""
src/pipeline.py
------------------------------------
End-to-end RAG orchestration for the AquaLogic system.

Flow:
  User Query + Feature Mode
        │
        ▼
  Retriever  ──► Vector Store (ChromaDB / FAISS)
        │          returns top-k policy chunks
        ▼
  Prompt Builder  ──► prompt_templates.py
        │               injects context + query
        ▼
  IBM Granite (watsonx.ai)
        │               generates grounded answer
        ▼
  AquaLogicResponse (answer + sources)
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import List

from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

from src.generation.prompt_templates import TEMPLATE_REGISTRY, format_prompt
from src.retrieval.retriever import Retriever

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("aqualogic.pipeline")

# ---------------------------------------------------------------------------
# Load environment variables (.env file)
# ---------------------------------------------------------------------------

load_dotenv()

# ---------------------------------------------------------------------------
# Response dataclass
# ---------------------------------------------------------------------------


@dataclass
class AquaLogicResponse:
    """Structured response returned by the RAG pipeline."""

    answer: str
    sources: List[str] = field(default_factory=list)
    feature_mode: str = ""
    query: str = ""

    def __str__(self) -> str:
        source_block = "\n".join(f"  • {s}" for s in self.sources) or "  • No sources retrieved."
        return (
            f"{'─' * 60}\n"
            f"Feature: {self.feature_mode}\n"
            f"Query:   {self.query}\n"
            f"{'─' * 60}\n"
            f"{self.answer}\n"
            f"{'─' * 60}\n"
            f"Sources:\n{source_block}\n"
        )


# ---------------------------------------------------------------------------
# AquaLogic RAG Pipeline
# ---------------------------------------------------------------------------


class AquaLogicPipeline:
    """
    Orchestrates the full RAG pipeline:
      1. Retrieve relevant policy chunks from the vector store.
      2. Build a grounded prompt using the appropriate feature template.
      3. Send the prompt to IBM Granite via watsonx.ai.
      4. Return a structured AquaLogicResponse.

    Args:
        retriever:      A Retriever instance wrapping the vector store.
        top_k:          Number of document chunks to retrieve per query.
        model_id:       IBM Granite model identifier on watsonx.ai.
        max_new_tokens: Maximum tokens for the generated response.
        temperature:    Sampling temperature (lower = more deterministic).
    """

    def __init__(
        self,
        retriever: Retriever,
        top_k: int = 5,
        model_id: str = "ibm/granite-13b-instruct-v2",
        max_new_tokens: int = 512,
        temperature: float = 0.3,
    ) -> None:
        self.retriever = retriever
        self.top_k = top_k

        # --- Initialise watsonx.ai credentials ---
        api_key = os.getenv("WATSONX_API_KEY")
        project_id = os.getenv("WATSONX_PROJECT_ID")
        url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

        if not api_key or not project_id:
            raise EnvironmentError(
                "WATSONX_API_KEY and WATSONX_PROJECT_ID must be set in your .env file."
            )

        credentials = Credentials(url=url, api_key=api_key)

        # --- Initialise the Granite model ---
        self.model = ModelInference(
            model_id=model_id,
            credentials=credentials,
            project_id=project_id,
            params={
                GenParams.MAX_NEW_TOKENS: max_new_tokens,
                GenParams.TEMPERATURE: temperature,
                GenParams.STOP_SEQUENCES: ["---"],   # prevent runaway generation
            },
        )

        logger.info("AquaLogicPipeline initialised | model=%s | top_k=%d", model_id, top_k)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, query: str, feature_mode: str = "jargon_translator") -> AquaLogicResponse:
        """
        Execute the full RAG pipeline for a user query.

        Args:
            query:        The user's natural-language question or input.
            feature_mode: Which AI feature to invoke. Must be one of:
                            - "jargon_translator"
                            - "policy_comparison"
                            - "checklist_generator"

        Returns:
            AquaLogicResponse containing the generated answer and source references.

        Raises:
            ValueError: If an unrecognised feature_mode is provided.
        """
        if feature_mode not in TEMPLATE_REGISTRY:
            raise ValueError(
                f"Unknown feature_mode '{feature_mode}'. "
                f"Choose from: {list(TEMPLATE_REGISTRY.keys())}"
            )

        # Document Retrieval Stage
        logger.info("Step 1/3 — Retrieving top-%d chunks for query: %r", self.top_k, query)
        retrieved_docs = self.retriever.retrieve(query, top_k=self.top_k)

        if not retrieved_docs:
            logger.warning("No documents retrieved. Returning grounded fallback response.")
            return AquaLogicResponse(
                answer=(
                    "I'm sorry, I could not find any relevant policy information for your query. "
                    "Please try rephrasing, or consult your local municipality directly."
                ),
                sources=[],
                feature_mode=feature_mode,
                query=query,
            )

        # Prompt Composition Stage
        logger.info("Step 2/3 — Building prompt using template: %s", feature_mode)
        context = self._build_context_block(retrieved_docs)
        template = TEMPLATE_REGISTRY[feature_mode]
        prompt = format_prompt(template=template, context=context, user_query=query)

        # LLM Inference Stage
        logger.info("Step 3/3 — Sending prompt to IBM Granite model.")
        response_text = self.model.generate_text(prompt=prompt)

        # Collect source metadata for citation
        sources = self._extract_sources(retrieved_docs)

        logger.info("Pipeline complete. Answer length: %d chars.", len(response_text))
        return AquaLogicResponse(
            answer=response_text.strip(),
            sources=sources,
            feature_mode=feature_mode,
            query=query,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_context_block(self, retrieved_docs: list) -> str:
        """
        Concatenate retrieved document chunks into a single context string.
        Each chunk is separated by a numbered marker for clarity.
        """
        parts = []
        for i, doc in enumerate(retrieved_docs, start=1):
            source_label = doc.metadata.get("source", "Unknown source")
            page_label = doc.metadata.get("page", "")
            header = f"[Chunk {i} | Source: {source_label}"
            if page_label:
                header += f", Page {page_label}"
            header += "]"
            parts.append(f"{header}\n{doc.page_content}")
        return "\n\n".join(parts)

    def _extract_sources(self, retrieved_docs: list) -> list[str]:
        """
        Extract a deduplicated list of source references from retrieved documents.
        """
        seen: set[str] = set()
        sources: list[str] = []
        for doc in retrieved_docs:
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "")
            ref = f"{source}, p.{page}" if page else source
            if ref not in seen:
                seen.add(ref)
                sources.append(ref)
        return sources


# ---------------------------------------------------------------------------
# Convenience factory: build pipeline from config.yaml
# ---------------------------------------------------------------------------


def build_pipeline_from_config(config_path: str = "configs/config.yaml") -> AquaLogicPipeline:
    """
    Instantiate the full AquaLogicPipeline by reading settings from config.yaml.

    Expects the following structure in config.yaml:
        model:
          id: "ibm/granite-13b-instruct-v2"
          max_new_tokens: 512
          temperature: 0.3
        retrieval:
          top_k: 5
          chunk_size: 512
          chunk_overlap: 64
        vector_store:
          provider: "chromadb"
          persist_directory: "./data/embeddings"
    """
    import yaml  # lazy import — only needed when using this factory

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    retriever = Retriever(
        provider=cfg["vector_store"]["provider"],
        persist_directory=cfg["vector_store"]["persist_directory"],
    )

    return AquaLogicPipeline(
        retriever=retriever,
        top_k=cfg["retrieval"]["top_k"],
        model_id=cfg["model"]["id"],
        max_new_tokens=cfg["model"]["max_new_tokens"],
        temperature=cfg["model"]["temperature"],
    )


# ---------------------------------------------------------------------------
# Quick smoke-test entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    pipeline = build_pipeline_from_config()

    # Example: Jargon-to-Action Translator
    response = pipeline.run(
        query="What does 'riparian water rights' mean for a small-scale farmer?",
        feature_mode="jargon_translator",
    )
    print(response)

    # Example: Policy Comparison Agent
    response = pipeline.run(
        query="Our factory discharges 300 litres of treated wastewater into the river daily.",
        feature_mode="policy_comparison",
    )
    print(response)

    # Example: Conservation Checklist Generator
    response = pipeline.run(
        query="I live in a household of 4 in Gauteng and mainly use water for domestic purposes.",
        feature_mode="checklist_generator",
    )
    print(response)
