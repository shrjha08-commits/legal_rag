import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from rank_bm25 import BM25Okapi

# 1. Initialize local Qdrant memory database and Embedding Model
# This model converts text into 384-dimensional mathematical vectors
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(":memory:")  # Runs completely in RAM for easy testing!

# 2. Load the structured chunks we made in Week 2
with open("structured_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# 3. Setup Vector Database Collection safely
COLLECTION_NAME = "legal_clauses"
if client.collection_exists(collection_name=COLLECTION_NAME):
    client.delete_collection(collection_name=COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# 4. Prepare and Upload Data to Vector DB
print("Indexing chunks into Vector DB...")
points = []
for idx, chunk in enumerate(chunks):
    # Combine parent context and text so the model understands both
    full_text_to_embed = f"Context: {chunk['parent_context']}\n{chunk['text']}"
    vector = model.encode(full_text_to_embed).tolist()
    
    points.append(
        PointStruct(
            id=idx,
            vector=vector,
            payload={"parent_context": chunk['parent_context'], "text": chunk['text']}
        )
    )

client.upsert(collection_name=COLLECTION_NAME, points=points)

# 5. Setup BM25 Keyword Search (The 'Hybrid' component)
# Dense vectors catch "meaning", BM25 catches exact words/numbers
tokenized_corpus = [chunk['text'].lower().split(" ") for chunk in chunks]
bm25 = BM25Okapi(tokenized_corpus)

print("🎯 Hybrid Search Engine initialized successfully!")

# 6. Define the Hybrid Search Function
def hybrid_search(query, top_k=1):
    print(f"\n🔍 Searching for: '{query}'")
    
    # 1. Generate the vector embeddings for the user question
    query_vector = model.encode(query).tolist()
    
    # 2. Pass that vector into the database using the correct 'query' argument name
    vector_results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,  # <-- FIXED THIS LINE from query_vector=query_vector
        limit=top_k
    )
    
    # 3. Return the best matched text payload
    if vector_results.points:
        best_match = vector_results.points[0].payload
        return f"[{best_match['parent_context']}] -> {best_match['text']}"
    return "No match found."

if __name__ == "__main__":
    # Test the system with a hyper-specific legal question
    result = hybrid_search("What is the monthly fee and when is it payable?")
    print("\n💡 Retracted Clause:")
    print(result)


    # ==========================================
# NEW CODES FOR SECONDARY TOOL (CASE LAW)
# ==========================================

# 1. Create a brand new collection for Historical Case Law precedents
CASE_COLLECTION = "case_law"
if client.collection_exists(collection_name=CASE_COLLECTION):
    client.delete_collection(collection_name=CASE_COLLECTION)

client.create_collection(
    collection_name=CASE_COLLECTION,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# 2. Load some mock case law history data
mock_cases = [
    {
        "parent_context": "Delaware Supreme Court (2018) - Smith v. Baker",
        "text": "The court ruled that monthly consulting retainers are strictly non-refundable once the business month commences, unless explicit material breach is shown."
    }
]

# 3. Index the case law data into the database
case_points = []
for idx, case in enumerate(mock_cases):
    full_text = f"Context: {case['parent_context']}\n{case['text']}"
    vector = model.encode(full_text).tolist()
    case_points.append(
        PointStruct(id=idx, vector=vector, payload=case)
    )
client.upsert(collection_name=CASE_COLLECTION, points=case_points)

# 4. Define the secondary search function
def case_law_search(query: str, top_k=1):
    query_vector = model.encode(query).tolist()
    results = client.query_points(collection_name=CASE_COLLECTION, query=query_vector, limit=top_k)
    if results.points:
        match = results.points[0].payload
        return f"[{match['parent_context']}] -> {match['text']}"
    return "No relevant case law found."