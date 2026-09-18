import sys
import os

sys.path.append(os.getcwd())

from src.generation.prompt_templates import TEMPLATE_REGISTRY, format_prompt

def simulate_aqualogic():
    print("AquaLogic Pipeline Diagnostic Tool v1.0")
    
    # 1. Simulate the User Input
    query = "What does 'riparian rights' mean for my farm?"
    print(f"\n[USER]: {query}")

    # 2. Simulate the 'Retriever' (Finding the data in a PDF)
    print("\n[SYSTEM]: Searching internal Policy PDFs...")
    mock_context = """
    [Chunk 1 | Source: Water Act 2023, Page 12]
    Riparian rights are the legal rights of owners of land bordering on a river or 
    other body of water to use the water for reasonable purposes. This includes 
    irrigation for small farms but requires a 'Usage Permit' if pumping exceeds 500L/day.
    """
    print("...Found relevant policy text in 'Water Act 2023'.")

    # 3. Choose the 'Feature' (Jargon Translator)
    feature = "jargon_translator"
    template = TEMPLATE_REGISTRY[feature]

    # 4. Format the Prompt (This is the most important AI part)
    final_prompt = format_prompt(template, mock_context, query)
    
    print("\n" + "="*50)
    print("DEBUG: Formatted Request Payload")
    print("="*50)
    print(final_prompt)
    print("="*50)

    # 5. Simulate the AI Response (What Granite would say)
    print("\nRESULT: Model Inference Output.")
    print("1. **Plain-Language Definition**: Riparian rights mean that because your farm is next to the river, you have a legal right to use that water.")
    print("2. **Why It Matters**: This rule ensures water is shared fairly among all neighbors on the river.")
    print("3. **What This Means For You**: You can use the water for your farm, but you must apply for a permit if you plan to pump more than 500 Liters a day.")

if __name__ == "__main__":
    simulate_aqualogic()