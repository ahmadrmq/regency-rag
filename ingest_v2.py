import ollama
import chromadb
import os
import pypdf

# --- CONFIGURATION ---
DB_PATH = "./regency_db"  # New Name
COLLECTION_NAME = "regency_knowledge"

print("--- INITIALIZING REGENCY INGESTION PROTOCOL ---")

# 1. SETUP DATABASE
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# 2. DEFINE SOURCE
folder_path = "knowledge_base"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Created {folder_path}. Put your PDFs here!")
    exit()

# 3. CRAWLER
files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
if not files:
    print("No PDFs found in knowledge_base/")
    exit()

print(f"--- DETECTED {len(files)} SOURCE FILES ---")

# 4. EXTRACTION LOOP
for filename in files:
    file_path = os.path.join(folder_path, filename)
    print(f"Processing: {filename}...")
    
    try:
        reader = pypdf.PdfReader(file_path)
        full_text = ""
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text += f"\n[Page {page_num + 1}]\n" + text
        
        # Chunking
        chunks = full_text.split("[Page")
        chunks = [f"[Page{c}" for c in chunks if len(c) > 50]
        
        # Embedding
        for i, chunk in enumerate(chunks):
            chunk_id = f"{filename}_chunk_{i}"
            response = ollama.embeddings(model='llama3', prompt=chunk)
            
            collection.add(
                ids=[chunk_id],
                embeddings=[response['embedding']],
                documents=[chunk],
                metadatas=[{"source": filename}]
            )
            print(f"  -> Indexed chunk {i+1}/{len(chunks)}", end='\r')
            
        print(f"\n  -> Completed {filename}.\n")

    except Exception as e:
        print(f"FAILED {filename}: {e}")

print("--- REGENCY KNOWLEDGE BASE UPDATED ---")