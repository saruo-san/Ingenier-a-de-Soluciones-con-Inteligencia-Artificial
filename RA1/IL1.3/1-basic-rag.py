import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="Basic RAG", page_icon="📚", layout="wide")

def initialize_client():
    client = OpenAI(
        base_url=os.getenv("GITHUB_BASE_URL", "https://models.inference.ai.azure.com"),
        api_key=os.getenv("GITHUB_TOKEN")
    )
    return client

def simple_retrieval(query, documents):
    relevant_docs = []
    query_lower = query.lower()
    
    for doc in documents:
        if any(word in doc.lower() for word in query_lower.split()):
            relevant_docs.append(doc)
    
    return relevant_docs[:3]

def generate_response(client, query, context):
    prompt = f"""Contexto:
{context}

Pregunta: {query}

Responde basándote únicamente en el contexto proporcionado. Si la información no está en el contexto, indica que no tienes esa información."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

def main():
    st.title("📚 RAG Básico")
    st.write("Sistema simple de Recuperación y Generación Aumentada")
    
    if "documents" not in st.session_state:
        st.session_state.documents = [
            "La inteligencia artificial es una rama de la informática que busca crear máquinas capaces de realizar tareas que requieren inteligencia humana.",
            "Los modelos de lenguaje grande (LLM) son sistemas de IA entrenados en enormes cantidades de texto para generar y comprender lenguaje natural.",
            "RAG (Retrieval-Augmented Generation) combina la búsqueda de información relevante con la generación de texto para producir respuestas más precisas.",
            "LangChain es un framework que facilita el desarrollo de aplicaciones con modelos de lenguaje, proporcionando herramientas para cadenas y agentes.",
            "El prompt engineering es la práctica de diseñar instrucciones efectivas para obtener los mejores resultados de los modelos de IA."
        ]
    
    st.sidebar.header("📄 Gestión de Documentos")
    
    new_doc = st.sidebar.text_area("Agregar nuevo documento:", height=100)
    if st.sidebar.button("Agregar Documento"):
        if new_doc.strip():
            st.session_state.documents.append(new_doc.strip())
            st.sidebar.success("Documento agregado!")
    
    st.sidebar.write(f"Total de documentos: {len(st.session_state.documents)}")
    
    if st.sidebar.button("Ver todos los documentos"):
        st.sidebar.write("**Documentos en la base:**")
        for i, doc in enumerate(st.session_state.documents, 1):
            st.sidebar.write(f"{i}. {doc[:50]}...")
    
    st.header("💬 Consulta")
    query = st.text_input("Haz tu pregunta:")
    
    if st.button("Buscar y Responder") and query:
        try:
            with st.spinner("Procesando..."):
                client = initialize_client()
                
                relevant_docs = simple_retrieval(query, st.session_state.documents)
                
                if relevant_docs:
                    context = "\n".join(relevant_docs)
                    
                    st.subheader("📋 Documentos Relevantes")
                    for i, doc in enumerate(relevant_docs, 1):
                        st.write(f"**{i}.** {doc}")
                    
                    response = generate_response(client, query, context)
                    
                    st.subheader("🤖 Respuesta")
                    st.write(response)
                else:
                    st.warning("No se encontraron documentos relevantes para tu consulta.")
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.header("ℹ️ Información del Sistema")
    with st.expander("Cómo funciona este RAG básico"):
        st.write("""
        **Componentes:**
        1. **Documentos**: Base de conocimiento simple en memoria
        2. **Retrieval**: Búsqueda por palabras clave
        3. **Generation**: Respuesta usando el contexto recuperado
        
        **Limitaciones:**
        - Búsqueda simple por coincidencia de palabras
        - No usa embeddings ni vectores
        - Almacenamiento temporal en sesión
        """)

if __name__ == "__main__":
    main()