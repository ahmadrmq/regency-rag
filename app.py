import streamlit as st
import ollama
import chromadb

# --- BRANDING CONFIG ---
st.set_page_config(
    page_title="Regency RAG",
    page_icon="🟦",
    layout="wide"
)

# --- BACKEND ---
@st.cache_resource
def get_database():
    client = chromadb.PersistentClient(path="./regency_db")
    return client.get_collection(name="regency_knowledge")

try:
    collection = get_database()
    db_status = "ONLINE"
    status_color = "green"
except:
    db_status = "OFFLINE (Run Ingestion)"
    status_color = "red"
    collection = None

# --- SIDEBAR ---
with st.sidebar:
    st.header("🟦 Regency RAG")
    st.caption("Local Engineering Intelligence")
    st.markdown("---")
    st.markdown(f"**Status:** :{status_color}[{db_status}]")
    st.markdown("**Hardware:** RTX 2060 12GB")
    
    if st.button("Flush Memory"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN UI ---
st.title("Regency Command")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Input command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        if collection:
            # Retrieval
            placeholder.markdown("`Accessing Archives...`")
            response = ollama.embeddings(model='llama3', prompt=prompt)
            results = collection.query(
                query_embeddings=[response['embedding']],
                n_results=3
            )
            
            combined_context = ""
            sources = []
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    doc = results['documents'][0][i]
                    meta = results['metadatas'][0][i]
                    source = meta.get('source', 'Unknown')
                    combined_context += f"\n--- SOURCE: {source} ---\n{doc}\n"
                    sources.append(source)
                
                with st.expander(f"📂 Referenced {len(set(sources))} Documents"):
                    st.code(combined_context)
            
            # Generation
            system_prompt = f"""
            You are REGENCY. An automated engineering assistant.
            Use the following context to answer the user.
            CONTEXT: {combined_context}
            """
            
            full_response = ""
            stream = ollama.chat(
                model='llama3',
                messages=[{'role': 'system', 'content': system_prompt}, 
                          {'role': 'user', 'content': prompt}],
                stream=True,
            )
            
            for chunk in stream:
                if chunk['message']['content']:
                    full_response += chunk['message']['content']
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            st.error("Database connection failed.")