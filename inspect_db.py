import chromadb

# Connect to the PDF database
client = chromadb.PersistentClient(path="./prince_db")
try:
    collection = client.get_collection(name="engineering_wisdom_v2")
except:
    print("Collection not found! Did you run ingest_v2.py?")
    exit()

# Get all data
data = collection.get()
ids = data['ids']
docs = data['documents']
metadatas = data['metadatas']

print(f"--- DATABASE DIAGNOSTIC: {len(ids)} CHUNKS FOUND ---")

if len(ids) == 0:
    print("CRITICAL ERROR: Database is empty.")
else:
    # Print the first 50 characters of every stored chunk
    print("\n--- CHUNK INVENTORY ---")
    for i, doc in enumerate(docs):
        # Clean up newlines for display
        preview = doc.replace('\n', ' ')[:60]
        source = metadatas[i]['source']
        print(f"[{i}] {source} | Content: {preview}...")

print("\n-----------------------")