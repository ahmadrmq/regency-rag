import ollama
import chromadb
import sys

# --- CONFIGURATION ---
DB_PATH = "./regency_db"
COLLECTION_NAME = "regency_knowledge"

print("--- INITIALIZING REGENCY CLI v1.0 ---")

try:
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)
    print("--- SYSTEM ONLINE: KNOWLEDGE BASE CONNECTED ---")
except Exception as e:
    print(f"--- ERROR: Database not found. Run ingest_v2.py first.")
    sys.exit()

messages = []

while True:
    try:
        user_input = input("\nUSER: ")
        if user_input.lower() in ['exit', 'quit']:
            break
    except KeyboardInterrupt:
        break

    print("REGENCY: Analyzing...", end='\r')
    
    # Retrieval
    response = ollama.embeddings(model='llama3', prompt=user_input)
    results = collection.query(
        query_embeddings=[response['embedding']],
        n_results=3
    )
    
    # Synthesis
    combined_context = ""
    if results['documents']:
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            source = meta.get('source', 'Unknown')
            combined_context += f"\n--- REF: {source} ---\n{doc}\n"
    else:
        combined_context = "No internal records found."

    # The New Persona
    system_instruction = f"""
    You are REGENCY, an advanced technical assistant.
    Your mandate is to answer questions using strictly the provided CONTEXT DATA.
    
    CONTEXT DATA:
    {combined_context}
    
    If the answer is not in the context, state that the archives are incomplete.
    """

    current_messages = messages.copy()
    current_messages.append({'role': 'system', 'content': system_instruction})
    current_messages.append({'role': 'user', 'content': user_input})

    response = ollama.chat(model='llama3', messages=current_messages)
    bot_reply = response['message']['content']
    
    print(f"REGENCY: {bot_reply}")
    
    messages.append({'role': 'user', 'content': user_input})
    messages.append({'role': 'assistant', 'content': bot_reply})