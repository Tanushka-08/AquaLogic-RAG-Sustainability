[ Citizen Query ] ──► [ RAG Pipeline ] ──► [ IBM Granite LLM ] ──► [ Simple Advice ]
                           │                    ▲
                           ▼                    │
                  [ ChromaDB Vector Store ] ────┘
                  (Municipal Policy PDFs)
                  
# 💧 AquaLogic RAG: Water Policy Assistant
> **A smart assistant using IBM Granite AI to make complex water laws understandable and actionable.**
> *A 1M1B AI for Sustainability Virtual Internship Project (SDG 6)*

---

## 🌍 The Problem
Water policies are written in "legalese"—complex language that regular people and small businesses cannot understand. This leads to accidental waste and non-compliance. **AquaLogic RAG** uses AI to "read" local laws and answer questions in simple, everyday language.

## ✨ Key Features
1. **Jargon-to-Action Translator**: Simplifies terms like "riparian rights."
2. **Policy Comparison Agent**: Checks if your current water usage matches local laws.
3. **Conservation Checklist**: Generates a custom "To-Do" list based on local scarcity levels.

## 🎯 SDG 6 Alignment
*   **Target 6.1 (Access):** Helps citizens understand their legal rights to water.
*   **Target 6.3 (Quality):** Surfaces rules for safe wastewater disposal.
*   **Target 6.4 (Efficiency):** Drives household savings through policy-based advice.
*   **Target 6.b (Participation):** Empowers non-technical citizens to participate in water governance.

## 🤖 Responsible AI & Ethics
*   **No Hallucinations:** Engineered with a strict fallback; if the answer isn't in the PDF, the AI says "I don't know."
*   **Transparency:** Every response includes a citation (e.g., "City Bylaw 2023, Section 4.2").

## 📁 IBM Bob Usage Evidence (Internship Requirement)
Following the guidelines, **IBM Bob AI** was used in the **Ideation and Planning phase**.
- **Designed** the modular file structure.
- **Mapped** features to SDG 6 targets.
- **Generated** the core Python orchestration logic.
*The `.bob` metadata folder is included in the root directory.*

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure WatsonX credentials in `.env`.