import os
from search_engine import hybrid_search

# 1. Simulate an Agent Tool
# This connects the search engine your brother just built directly to the LLM's brain
def legal_knowledge_base_tool(user_query: str) -> str:
    """Useful for searching legal contract details, compensation, service durations, and clauses."""
    return hybrid_search(user_query)

# 2. The Agent Logic (Simplest implementation of the LLM Compiler planner concept)
def legal_agent(user_prompt: str):
    print(f"\n🚀 Agent Received Task: '{user_prompt}'")
    
    # Step A: The "Planning" Phase
    # In an LLM Compiler, the LLM decides which tools are needed.
    # We will simulate a quick routing check: Does the query require contract search?
    print("🧠 Planning Phase: Analyzing query dependencies...")
    
    # If the user is asking about the contract, use our tool
    if any(word in user_prompt.lower() for word in ["fee", "pay", "service", "clause", "terminate", "agreement"]):
        print("🛠️ Execution Phase: Triggering 'legal_knowledge_base_tool'...")
        context_retrieved = legal_knowledge_base_tool(user_prompt)
        
        # Step B: The "Joiner" Phase
        # Normally an LLM would synthesize this context. Here we print the raw execution pipeline stream:
        print("\n✨ Final Agent Synthesis:")
        print(f"Based on the contract execution data retrieved: {context_retrieved}")
    else:
        print("❌ Execution Phase: Query does not match legal document tools.")

if __name__ == "__main__":
    # Test the agent loop!
    legal_agent("Check the agreement and tell me how much the client has to pay.")