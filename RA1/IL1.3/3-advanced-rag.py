import streamlit as st
import os
import json
from datetime import datetime
from openai import OpenAI
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Advanced RAG", page_icon="🧠", layout="wide")

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

def hybrid_search(query, documents, embeddings, client, top_k=5):
    query_embedding = get_embeddings(client, [query])[0]
    
    semantic_similarities = cosine_similarity([query_embedding], embeddings)[0]
    
    keyword_scores = []
    query_words = set(query.lower().split())
    for doc in documents:
        doc_words = set(doc.lower().split())
        overlap = len(query_words.intersection(doc_words))
        keyword_scores.append(overlap / max(len(query_words), 1))
    
    combined_scores = 0.7 * semantic_similarities + 0.3 * np.array(keyword_scores)
    
    top_indices = np.argsort(combined_scores)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        results.append({
            'document': documents[idx],
            'semantic_score': semantic_similarities[idx],
            'keyword_score': keyword_scores[idx],
            'combined_score': combined_scores[idx],
            'index': idx
        })
    
    return results

def rerank_results(client, query, results, top_k=3):
    rerank_prompt = f"""Dada la consulta: "{query}"
    
Evalúa qué tan relevante es cada documento para responder la consulta. 
Asigna una puntuación de 0-10 donde 10 es extremadamente relevante.

Documentos:
"""
    
    for i, result in enumerate(results):
        rerank_prompt += f"\n{i+1}. {result['document'][:200]}...\n"
    
    rerank_prompt += "\nResponde SOLO con números separados por comas (ej: 8,5,9,2,7):"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": rerank_prompt}],
            temperature=0.1,
            max_tokens=50
        )
        
        scores = [float(x.strip()) for x in response.choices[0].message.content.split(',')]
        
        for i, score in enumerate(scores[:len(results)]):
            results[i]['rerank_score'] = score
        
        reranked = sorted(results, key=lambda x: x.get('rerank_score', 0), reverse=True)
        return reranked[:top_k]
        
    except:
        return results[:top_k]

def query_expansion(client, query):
    expansion_prompt = f"""Dado esta consulta: "{query}"

Genera 3 consultas relacionadas que podrían ayudar a encontrar información complementaria.
Las consultas deben ser variaciones semánticas o aspectos relacionados.

Responde SOLO con las 3 consultas, una por línea:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": expansion_prompt}],
            temperature=0.7,
            max_tokens=150
        )
        
        expanded_queries = [q.strip() for q in response.choices[0].message.content.split('\n') if q.strip()]
        return [query] + expanded_queries[:3]
        
    except:
        return [query]

def generate_response_with_memory(client, query, context_docs, conversation_history):
    history_context = ""
    if conversation_history:
        recent_history = conversation_history[-3:]
        history_context = "\n".join([f"Q: {h['query']}\nA: {h['response'][:200]}..." 
                                   for h in recent_history])
    
    context = "\n\n".join([f"Documento {i+1} (Relevancia: {doc.get('rerank_score', doc['combined_score']):.2f}): {doc['document']}" 
                          for i, doc in enumerate(context_docs)])
    
    prompt = f"""Historial de conversación reciente:
{history_context}

Contexto relevante para la consulta actual:
{context}

Consulta actual: {query}

Instrucciones:
- Responde basándote principalmente en el contexto proporcionado
- Considera el historial de conversación para mantener coherencia
- Si haces referencia a información previa, indícalo claramente
- Si la información no está completa, sugiere qué información adicional sería útil
- Cita los documentos más relevantes usados"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )
    
    return response.choices[0].message.content

def save_conversation(query, response, context_docs):
    conversation_entry = {
        'timestamp': datetime.now().isoformat(),
        'query': query,
        'response': response,
        'context_used': len(context_docs),
        'top_scores': [doc.get('rerank_score', doc['combined_score']) for doc in context_docs[:3]]
    }
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    st.session_state.conversation_history.append(conversation_entry)

def main():
    st.title("🧠 RAG Avanzado")
    st.write("Sistema RAG con búsqueda híbrida, re-ranking, expansión de consultas y memoria")
    
    if "advanced_rag" not in st.session_state:
        st.session_state.advanced_rag = {
            'documents': [],
            'embeddings': None,
            'use_query_expansion': True,
            'use_reranking': True,
            'hybrid_weights': {'semantic': 0.7, 'keyword': 0.3}
        }
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    client = initialize_client()
    
    st.sidebar.header("🔧 Configuración Avanzada")
    
    st.session_state.advanced_rag['use_query_expansion'] = st.sidebar.checkbox(
        "Expansión de consultas", 
        value=st.session_state.advanced_rag['use_query_expansion']
    )
    
    st.session_state.advanced_rag['use_reranking'] = st.sidebar.checkbox(
        "Re-ranking con LLM", 
        value=st.session_state.advanced_rag['use_reranking']
    )
    
    st.sidebar.subheader("Pesos de búsqueda híbrida")
    semantic_weight = st.sidebar.slider("Peso semántico:", 0.0, 1.0, 0.7, 0.1)
    keyword_weight = 1.0 - semantic_weight
    st.session_state.advanced_rag['hybrid_weights'] = {
        'semantic': semantic_weight, 
        'keyword': keyword_weight
    }
    st.sidebar.write(f"Peso palabras clave: {keyword_weight:.1f}")
    
    st.sidebar.header("📄 Gestión de Documentos")
    
    uploaded_files = st.sidebar.file_uploader(
        "Subir múltiples archivos", 
        type=['txt'], 
        accept_multiple_files=True
    )
    
    if uploaded_files and st.sidebar.button("Procesar Archivos"):
        with st.spinner("Procesando archivos..."):
            new_docs = []
            for file in uploaded_files:
                content = file.read().decode('utf-8')
                chunks = content.split('\n\n')
                new_docs.extend([chunk.strip() for chunk in chunks if chunk.strip()])
            
            st.session_state.advanced_rag['documents'].extend(new_docs)
            st.session_state.advanced_rag['embeddings'] = None
            st.sidebar.success(f"Procesados {len(new_docs)} chunks de {len(uploaded_files)} archivos")
    
    manual_doc = st.sidebar.text_area("Documento manual:", height=100)
    if st.sidebar.button("Agregar Manual") and manual_doc.strip():
        st.session_state.advanced_rag['documents'].append(manual_doc.strip())
        st.session_state.advanced_rag['embeddings'] = None
        st.sidebar.success("Documento agregado")
    
    if st.sidebar.button("🔄 Generar Embeddings"):
        if st.session_state.advanced_rag['documents']:
            with st.spinner("Generando embeddings..."):
                try:
                    embeddings = get_embeddings(client, st.session_state.advanced_rag['documents'])
                    st.session_state.advanced_rag['embeddings'] = embeddings
                    st.sidebar.success("Embeddings generados!")
                except Exception as e:
                    st.sidebar.error(f"Error: {str(e)}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Consulta Inteligente")
        
        query = st.text_input("Haz tu pregunta:")
        
        col_a, col_b = st.columns(2)
        with col_a:
            top_k_search = st.slider("Documentos a buscar:", 3, 15, 8)
        with col_b:
            top_k_final = st.slider("Documentos finales:", 1, 5, 3)
        
        if st.button("🚀 Búsqueda Avanzada") and query:
            if not st.session_state.advanced_rag['documents']:
                st.warning("No hay documentos en la base.")
            elif st.session_state.advanced_rag['embeddings'] is None:
                st.warning("Genera los embeddings primero.")
            else:
                try:
                    with st.spinner("Procesando consulta avanzada..."):
                        queries_to_search = [query]
                        
                        if st.session_state.advanced_rag['use_query_expansion']:
                            st.info("🔍 Expandiendo consulta...")
                            expanded = query_expansion(client, query)
                            queries_to_search = expanded
                            
                            with st.expander("Consultas expandidas"):
                                for i, q in enumerate(expanded):
                                    st.write(f"{i+1}. {q}")
                        
                        all_results = []
                        for search_query in queries_to_search:
                            results = hybrid_search(
                                search_query, 
                                st.session_state.advanced_rag['documents'],
                                st.session_state.advanced_rag['embeddings'],
                                client,
                                top_k_search
                            )
                            all_results.extend(results)
                        
                        seen_docs = set()
                        unique_results = []
                        for result in all_results:
                            doc_key = result['document'][:100]
                            if doc_key not in seen_docs:
                                seen_docs.add(doc_key)
                                unique_results.append(result)
                        
                        if st.session_state.advanced_rag['use_reranking']:
                            st.info("🎯 Re-ranking con LLM...")
                            final_results = rerank_results(client, query, unique_results[:top_k_search], top_k_final)
                        else:
                            final_results = sorted(unique_results, key=lambda x: x['combined_score'], reverse=True)[:top_k_final]
                        
                        st.subheader("📋 Documentos Seleccionados")
                        for i, result in enumerate(final_results):
                            score_info = f"Semántico: {result['semantic_score']:.3f}, "
                            score_info += f"Palabras clave: {result['keyword_score']:.3f}, "
                            score_info += f"Combinado: {result['combined_score']:.3f}"
                            if 'rerank_score' in result:
                                score_info += f", Re-rank: {result['rerank_score']:.1f}"
                            
                            with st.expander(f"Documento {i+1} - {score_info}"):
                                st.write(result['document'])
                        
                        response = generate_response_with_memory(
                            client, query, final_results, st.session_state.conversation_history
                        )
                        
                        st.subheader("🤖 Respuesta")
                        st.write(response)
                        
                        save_conversation(query, response, final_results)
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        st.header("📊 Estado del Sistema")
        st.metric("Documentos", len(st.session_state.advanced_rag['documents']))
        st.metric("Conversaciones", len(st.session_state.conversation_history))
        
        if st.session_state.advanced_rag['embeddings'] is not None:
            st.success("✅ Embeddings listos")
        else:
            st.warning("⏳ Embeddings pendientes")
        
        st.header("💬 Historial")
        if st.session_state.conversation_history:
            for i, conv in enumerate(reversed(st.session_state.conversation_history[-5:])):
                with st.expander(f"Consulta {len(st.session_state.conversation_history)-i}"):
                    st.write(f"**P:** {conv['query']}")
                    st.write(f"**R:** {conv['response'][:150]}...")
                    st.write(f"**Docs usados:** {conv['context_used']}")
        
        if st.button("🗑️ Limpiar Historial"):
            st.session_state.conversation_history = []
            st.success("Historial limpiado")
        
        st.header("ℹ️ Características")
        with st.expander("Funcionalidades avanzadas"):
            st.write("""
            **🔍 Búsqueda Híbrida:**
            - Combina similitud semántica y coincidencia de palabras clave
            
            **🎯 Re-ranking:**
            - LLM evalúa relevancia de documentos recuperados
            
            **🔄 Expansión de consultas:**
            - Genera variaciones para búsqueda más amplia
            
            **🧠 Memoria conversacional:**
            - Mantiene contexto de consultas anteriores
            
            **⚙️ Configuración dinámica:**
            - Ajuste de pesos y parámetros en tiempo real
            """)

if __name__ == "__main__":
    main()