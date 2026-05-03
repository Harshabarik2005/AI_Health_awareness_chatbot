import asyncio
import sys
from pathlib import Path

# Add backend to sys.path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from app.services.retrieval import retrieve_context, format_context_for_prompt
from app.services.llm import generate_response

async def test_chat(query: str):
    print(f"\n[USER QUERY]: {query}")
    print("-" * 50)
    
    # Retrieval
    chunks = retrieve_context(query)
    context_block = format_context_for_prompt(chunks)
    
    print("[CONTEXT RETRIEVED]:")
    print(context_block[:300] + ("...\n" if len(context_block) > 300 else "\n"))
    
    print("[AI DIAGNOSING...]")
    
    # LLM Generate
    response = await generate_response(query, context_block)
    
    print("[AI RESPONSE]:")
    print(response)
    print("=" * 50)

async def main():
    test_cases = [
        "I'm facing severe knee pain and mild fever, why is it happening?",
        "How is HIV transmitted?"
    ]
    for tc in test_cases:
        await test_chat(tc)

if __name__ == "__main__":
    asyncio.run(main())
