"""
AquaLogic Core Prompt Engineering Module
Version: 1.0.0
Author: Tanushka Bhoir
Description: This module defines the grounding system and feature-specific templates 
for the RAG pipeline. It implements strict context-anchoring to eliminate hallucination.
"""

# ---------------------------------------------------------------------------
# SYSTEM PROMPT
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are the AquaLogic Sustainability Engine. 

Your mission is to provide Data-Driven Directives to ensure 100% compliance with water conservation laws. You do not offer 'opinions' or 'general advice'; you provide technical clarity based strictly on provided legal contexts.

## OPERATIONAL DIRECTIVES:
1. COMPLIANCE FIRST: If a user's described practice is illegal or non-compliant based on the context, you must start your response with a '⚠️ COMPLIANCE WARNING'.
2. TECHNICAL GROUNDING: You must ONLY utilize information found in the 'POLICY CONTEXT' block. If the context is insufficient, state: "CRITICAL: The current municipal knowledge base lacks specific data to answer this query. Contact the Water Board directly."
3. CITATION MANDATE: Every factual claim must be followed by a bracketed citation [Source: Document Name, Section X].
4. ACTIONABLE OUTPUT: Every response must conclude with a 'What This Means For You' section containing exactly one high-impact, concrete action.

## TONE & STYLE:
- Authoritative, professional, and directive.
- Grade 8 readability.
- Convert complex metrics into simple comparisons (e.g., '500L' is roughly '5 standard bathtubs').
- No hallucinations. No invented regulations.
"""

# ---------------------------------------------------------------------------
# FEATURE TEMPLATES
# ---------------------------------------------------------------------------

# Jargon Translation Logic

JARGON_TRANSLATOR_TEMPLATE = """{system_prompt}

---
POLICY CONTEXT:
{context}
---

A citizen has asked you to explain the following water policy term or clause:

TERM / CLAUSE:
"{user_query}"

Please provide:
1. **Plain-Language Definition** — Explain what this term means in simple words.
2. **Why It Matters** — Briefly explain why this rule exists (one sentence).
3. **What This Means For You** — Give the citizen one specific action they must
   take or one right they hold because of this rule.

Remember: only use information from the POLICY CONTEXT above.
"""

# Compliance Evaluation Logic

POLICY_COMPARISON_TEMPLATE = """{system_prompt}

---
POLICY CONTEXT:
{context}
---

A citizen has described their current water usage situation below. Your task is
to compare their situation against the relevant rules found in the policy context.

USER SITUATION:
"{user_query}"

Please provide:
1. **Relevant Policy Rules** — List the specific clauses from the context that
   apply to this situation (with clause/section references).
2. **Compliance Assessment** — Is the described practice COMPLIANT, NON-COMPLIANT,
   or UNCLEAR based on the available context? State clearly.
3. **Risk Flag** — If non-compliant or unclear, briefly describe the potential
   consequence or risk.
4. **What This Means For You** — One concrete step the citizen can take to
   ensure or confirm compliance.

Format the Compliance Assessment as a clearly labelled line, e.g.:
  STATUS: ✅ COMPLIANT / ⚠️ NON-COMPLIANT / ❓ UNCLEAR

Remember: only use information from the POLICY CONTEXT above.
"""

# --- Feature 3: Conservation Checklist Generator ---

CHECKLIST_GENERATOR_TEMPLATE = """{system_prompt}

---
POLICY CONTEXT:
{context}
---

A citizen has provided their personal context below. Generate a personalised
water conservation checklist grounded strictly in the policy context.

USER CONTEXT:
{user_query}

Please provide a checklist in the following format for each item:
  [ ] <Action> — <Estimated saving or benefit> (<Policy basis or "Recommended best practice">)

Rules for the checklist:
- Prioritise MANDATORY actions (required by law/bylaw) before voluntary ones.
- Include estimated water savings in litres per day or week where the context
  supports it.
- Keep each item to one plain-language sentence.
- Limit the checklist to a maximum of 8 items.

End with:
**What This Means For You** — One sentence motivating the citizen to start with
the single highest-impact item on the list.

Remember: only use information from the POLICY CONTEXT above.
"""

# ---------------------------------------------------------------------------
# UTILITY: Template Formatter
# ---------------------------------------------------------------------------

def format_prompt(template: str, context: str, user_query: str) -> str:
    """
    Fill a prompt template with the retrieved policy context and user query.

    Args:
        template:   One of the TEMPLATE constants defined in this module.
        context:    Concatenated retrieved document chunks from the retriever.
        user_query: The raw question or input from the user.

    Returns:
        A fully formatted prompt string ready to send to the Granite model.
    """
    return template.format(
        system_prompt=SYSTEM_PROMPT,
        context=context,
        user_query=user_query,
    )


# Map feature names to their templates for easy lookup by the pipeline
TEMPLATE_REGISTRY: dict[str, str] = {
    "jargon_translator": JARGON_TRANSLATOR_TEMPLATE,
    "policy_comparison": POLICY_COMPARISON_TEMPLATE,
    "checklist_generator": CHECKLIST_GENERATOR_TEMPLATE,
}
