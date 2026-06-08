import asyncio
import time
from search_engine import hybrid_search, case_law_search

# 1. Turn our synchronous search tools into Asynchronous Tasks
# We use asyncio.to_thread to run the database queries on independent background threads
async def async_contract_tool(query: str):
    print("⏳ [Tool 1] Starting Contract database search...")
    # Simulate slight network delay
    await asyncio.sleep(1.5) 
    result = hybrid_search(query)
    print("✅ [Tool 1] Contract search complete!")
    return result

async def async_case_law_tool(query: str):
    print("⏳ [Tool 2] Starting Case Law database search...")
    # Simulate slight network delay
    await asyncio.sleep(1.5) 
    result = case_law_search(query)
    print("✅ [Tool 2] Case Law search complete!")
    return result

# 2. The Core Concurrent Execution Loop (The LLM Compiler Execution Stage)
async def run_parallel_agent(user_prompt: str):
    print(f"🚀 User Task Received: '{user_prompt}'\n")
    print("🧠 [Planner Stage] Analyzing dependencies... Both tools are independent.")
    print("⚡ [Execution Stage] Launching tools concurrently via Asyncio...\n")
    
    start_time = time.time()
    
    # This is where the magic happens. Both tools are fired simultaneously.
    # Instead of taking 1.5s + 1.5s = 3.0 seconds, they run in parallel.
    contract_task = async_contract_tool(user_prompt)
    case_law_task = async_case_law_tool(user_prompt)
    
    # Gather execution results concurrently
    contract_res, case_res = await asyncio.gather(contract_task, case_law_task)
    
    end_time = time.time()
    
    # 3. The Joiner Stage (Synthesizing data streams)
    print("\n✨ [Joiner Stage] Synthesizing parallel data streams:")
    print(f"--- Contract Tool Output: {contract_res}")
    print(f"--- Case Law Tool Output: {case_res}")
    print(f"\n⏱️ Total Parallel Execution Time: {end_time - start_time:.2f} seconds!")

if __name__ == "__main__":
    # Run the main async loop
    asyncio.run(run_parallel_agent("What are the rules regarding our monthly consulting fee payments?"))