import streamlit as st
import os
import numpy as np
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

st.set_page_config(page_title="Vector RAG", page_icon="🔍", layout="wide")

def initialize_client():
    client = OpenAI(
        base_url=os.getenv("GITHUB_BASE_URL", "https://models.inference.ai.azure.com"),
        api_key=os.getenv("GITHUB_TOKEN")
    )
    return client

def get_embeddings(client, texts):
    embeddings = []
    for text in texts:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        embeddings.append(response.data[0].embedding)
    return np.array(embeddings)

def vector_search(query_embedding, doc_embeddings, documents, top_k=3):
    similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        results.append({
            'document': documents[idx],
            'similarity': similarities[idx],
            'index': idx
        })
    return results

def chunking_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        
        if i + chunk_size >= len(words):
            break
    
    return chunks

def generate_response(client, query, context_docs):
    context = "\n\n".join([f"Documento {i+1}: {doc['document']}" 
                          for i, doc in enumerate(context_docs)])
    
    prompt = f"""Contexto relevante:
{context}

Pregunta: {query}

Instrucciones:
- Responde basándote en el contexto proporcionado
- Si la información no está completa, menciona qué información adicional sería útil
- Cita qué documento(s) usaste para responder"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=600
    )
    
    return response.choices[0].message.content

def main():
    st.title("🔍 RAG con Vectores")
    st.write("Sistema de RAG usando embeddings y búsqueda semántica")
    
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = {
            'documents': [],
            'embeddings': None,
            'vectorizer': None
        }
    
    client = initialize_client()
    
    st.sidebar.header("📄 Gestión de Documentos")
    
    upload_method = st.sidebar.radio("Método de carga:", ["Texto manual", "Archivo"])
    
    if upload_method == "Texto manual":
        new_doc = st.sidebar.text_area("Agregar documento:", height=150)
        chunk_option = st.sidebar.checkbox("Dividir en chunks", value=True)
        
        if st.sidebar.button("Procesar Documento"):
            if new_doc.strip():
                with st.spinner("Procesando documento..."):
                    if chunk_option:
                        chunks = chunking_text(new_doc.strip())
                        st.session_state.vector_store['documents'].extend(chunks)
                        st.sidebar.success(f"Documento dividido en {len(chunks)} chunks")
                    else:
                        st.session_state.vector_store['documents'].append(new_doc.strip())
                        st.sidebar.success("Documento agregado")
                    
                    st.session_state.vector_store['embeddings'] = None
    
    else:
        uploaded_file = st.sidebar.file_uploader("Subir archivo", type=['txt'])
        if uploaded_file and st.sidebar.button("Procesar Archivo"):
            content = uploaded_file.read().decode('utf-8')
            chunks = chunking_text(content)
            st.session_state.vector_store['documents'].extend(chunks)
            st.sidebar.success(f"Archivo procesado en {len(chunks)} chunks")
            st.session_state.vector_store['embeddings'] = None
    
    st.sidebar.write(f"Total documentos: {len(st.session_state.vector_store['documents'])}")
    
    if st.sidebar.button("🔄 Generar Embeddings"):
        if st.session_state.vector_store['documents']:
            with st.spinner("Generando embeddings..."):
                try:
                    embeddings = get_embeddings(client, st.session_state.vector_store['documents'])
                    st.session_state.vector_store['embeddings'] = embeddings
                    st.sidebar.success("Embeddings generados!")
                except Exception as e:
                    st.sidebar.error(f"Error generando embeddings: {str(e)}")
    
    if st.sidebar.button("Limpiar Base"):
        st.session_state.vector_store = {
            'documents': [],
            'embeddings': None,
            'vectorizer': None
        }
        st.sidebar.success("Base limpiada")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Consulta Semántica")
        query = st.text_input("Haz tu pregunta:")
        similarity_threshold = st.slider("Umbral de similitud:", 0.0, 1.0, 0.3, 0.1)
        top_k = st.slider("Número de documentos a recuperar:", 1, 10, 3)
        
        if st.button("🔍 Buscar y Responder") and query:
            if not st.session_state.vector_store['documents']:
                st.warning("No hay documentos en la base. Agrega algunos primero.")
            elif st.session_state.vector_store['embeddings'] is None:
                st.warning("Genera los embeddings primero usando el botón en la barra lateral.")
            else:
                try:
                    with st.spinner("Buscando información relevante..."):
                        query_embedding = get_embeddings(client, [query])[0]
                        
                        results = vector_search(
                            query_embedding, 
                            st.session_state.vector_store['embeddings'],
                            st.session_state.vector_store['documents'],
                            top_k
                        )
                        
                        filtered_results = [r for r in results if r['similarity'] > similarity_threshold]
                        
                        if filtered_results:
                            st.subheader("📋 Documentos Relevantes")
                            for i, result in enumerate(filtered_results):
                                with st.expander(f"Documento {i+1} (Similitud: {result['similarity']:.3f})"):
                                    st.write(result['document'])
                            
                            response = generate_response(client, query, filtered_results)
                            
                            st.subheader("🤖 Respuesta")
                            st.write(response)
                        else:
                            st.warning(f"No se encontraron documentos con similitud > {similarity_threshold}")
                            
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        st.header("📊 Estadísticas")
        if st.session_state.vector_store['documents']:
            st.metric("Documentos", len(st.session_state.vector_store['documents']))
            
            if st.session_state.vector_store['embeddings'] is not None:
                st.metric("Dimensión embeddings", st.session_state.vector_store['embeddings'].shape[1])
                st.success("✅ Embeddings listos")
            else:
                st.warning("⏳ Embeddings pendientes")
        
        st.header("ℹ️ Información")
        with st.expander("Cómo funciona"):
            st.write("""
            **Mejoras sobre RAG básico:**
            1. **Embeddings**: Representación vectorial semántica
            2. **Chunking**: División inteligente de textos largos
            3. **Similitud coseno**: Búsqueda más precisa
            4. **Umbral configurable**: Control de relevancia
            5. **Carga de archivos**: Procesamiento de documentos externos
            
            **Proceso:**
            1. Los documentos se convierten en vectores (embeddings)
            2. La consulta también se vectoriza
            3. Se calcula similitud coseno entre consulta y documentos
            4. Se seleccionan los más similares para generar respuesta
            """)

if __name__ == "__main__":
    main()