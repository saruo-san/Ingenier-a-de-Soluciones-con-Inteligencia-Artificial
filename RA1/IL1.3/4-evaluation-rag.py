import streamlit as st
import os
import json
import time
import uuid
from datetime import datetime
import pandas as pd
import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="RAG Evaluation", page_icon="📊", layout="wide")

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

def evaluate_faithfulness(client, query, context, response):
    eval_prompt = f"""Evalúa si la respuesta es fiel al contexto proporcionado.

Consulta: {query}

Contexto:
{context}

Respuesta:
{response}

¿La respuesta está basada únicamente en la información del contexto? 
Responde con un número del 1-10 donde:
- 1-3: Respuesta contradice o no está basada en el contexto
- 4-6: Respuesta parcialmente basada en el contexto
- 7-10: Respuesta completamente fiel al contexto

Responde SOLO con el número:"""

    try:
        result = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": eval_prompt}],
            temperature=0.1,
            max_tokens=10
        )
        return float(result.choices[0].message.content.strip())
    except:
        return 5.0

def evaluate_relevance(client, query, response):
    eval_prompt = f"""Evalúa qué tan relevante es la respuesta para la consulta.

Consulta: {query}

Respuesta: {response}

¿Qué tan bien responde la respuesta a la consulta?
Responde con un número del 1-10 donde:
- 1-3: Respuesta no relacionada o irrelevante
- 4-6: Respuesta parcialmente relevante
- 7-10: Respuesta muy relevante y útil

Responde SOLO con el número:"""

    try:
        result = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": eval_prompt}],
            temperature=0.1,
            max_tokens=10
        )
        return float(result.choices[0].message.content.strip())
    except:
        return 5.0

def evaluate_context_precision(client, query, retrieved_docs):
    if not retrieved_docs:
        return 0.0
    
    relevant_count = 0
    for doc in retrieved_docs:
        eval_prompt = f"""¿Este documento es relevante para responder la consulta?

Consulta: {query}

Documento: {doc['document'][:300]}...

Responde SOLO 'SI' o 'NO':"""
        
        try:
            result = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": eval_prompt}],
                temperature=0.1,
                max_tokens=5
            )
            if result.choices[0].message.content.strip().upper() == 'SI':
                relevant_count += 1
        except:
            pass
    
    return relevant_count / len(retrieved_docs)

def hybrid_search_with_metrics(query, documents, embeddings, client, top_k=5):
    start_time = time.time()
    
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
    
    retrieval_time = time.time() - start_time
    
    return results, retrieval_time

def generate_response_with_metrics(client, query, context_docs):
    start_time = time.time()
    
    context = "\n\n".join([f"Documento {i+1}: {doc['document']}" 
                          for i, doc in enumerate(context_docs)])
    
    prompt = f"""Contexto:
{context}

Pregunta: {query}

Responde basándote únicamente en el contexto proporcionado."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=600
    )
    
    generation_time = time.time() - start_time
    response_text = response.choices[0].message.content
    
    return response_text, generation_time

def create_evaluation_dataset():
    return [
        {
            "query": "¿Qué es la inteligencia artificial?",
            "expected_context": "definición de IA",
            "ground_truth": "La inteligencia artificial es una rama de la informática que busca crear máquinas capaces de realizar tareas que requieren inteligencia humana."
        },
        {
            "query": "¿Cómo funciona RAG?",
            "expected_context": "funcionamiento de RAG",
            "ground_truth": "RAG combina la búsqueda de información relevante con la generación de texto para producir respuestas más precisas."
        },
        {
            "query": "¿Qué es LangChain?",
            "expected_context": "descripción de LangChain",
            "ground_truth": "LangChain es un framework que facilita el desarrollo de aplicaciones con modelos de lenguaje."
        }
    ]

def log_interaction(query, response, metrics, context_docs):
    if 'interaction_logs' not in st.session_state:
        st.session_state.interaction_logs = []
    
    log_entry = {
        'id': str(uuid.uuid4()),
        'timestamp': datetime.now().isoformat(),
        'query': query,
        'response': response,
        'metrics': metrics,
        'context_count': len(context_docs),
        'context_scores': [doc.get('combined_score', 0) for doc in context_docs]
    }
    
    st.session_state.interaction_logs.append(log_entry)

def export_langsmith_format(logs):
    langsmith_data = []
    for log in logs:
        langsmith_data.append({
            "run_id": log['id'],
            "timestamp": log['timestamp'],
            "inputs": {"query": log['query']},
            "outputs": {"response": log['response']},
            "metrics": log['metrics'],
            "metadata": {
                "context_count": log['context_count'],
                "context_scores": log['context_scores']
            }
        })
    return langsmith_data

def main():
    st.title("📊 RAG con Evaluación y Monitoreo")
    st.write("Sistema RAG con métricas detalladas y capacidades de evaluación")
    
    if "eval_rag" not in st.session_state:
        st.session_state.eval_rag = {
            'documents': [
                "La inteligencia artificial es una rama de la informática que busca crear máquinas capaces de realizar tareas que requieren inteligencia humana.",
                "Los modelos de lenguaje grande (LLM) son sistemas de IA entrenados en enormes cantidades de texto para generar y comprender lenguaje natural.",
                "RAG (Retrieval-Augmented Generation) combina la búsqueda de información relevante con la generación de texto para producir respuestas más precisas.",
                "LangChain es un framework que facilita el desarrollo de aplicaciones con modelos de lenguaje, proporcionando herramientas para cadenas y agentes.",
                "El prompt engineering es la práctica de diseñar instrucciones efectivas para obtener los mejores resultados de los modelos de IA.",
                "Los embeddings son representaciones vectoriales de texto que capturan el significado semántico en un espacio multidimensional.",
                "La búsqueda semántica utiliza embeddings para encontrar contenido relacionado por significado, no solo por palabras clave.",
                "Los sistemas de evaluación de IA miden métricas como relevancia, fidelidad y precisión del contexto."
            ],
            'embeddings': None,
            'enable_logging': True
        }
    
    if 'interaction_logs' not in st.session_state:
        st.session_state.interaction_logs = []
    
    client = initialize_client()
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Consulta", "📊 Métricas", "🧪 Evaluación", "📈 Analytics"])
    
    with tab1:
        st.header("💬 Consulta con Monitoreo")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query = st.text_input("Haz tu pregunta:")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                top_k = st.slider("Docs a recuperar:", 1, 8, 3)
            with col_b:
                eval_enabled = st.checkbox("Evaluación automática", value=True)
            with col_c:
                st.session_state.eval_rag['enable_logging'] = st.checkbox("Logging", value=True)
        
        with col2:
            if st.button("🔄 Generar Embeddings"):
                if st.session_state.eval_rag['documents']:
                    with st.spinner("Generando embeddings..."):
                        embeddings = get_embeddings(client, st.session_state.eval_rag['documents'])
                        st.session_state.eval_rag['embeddings'] = embeddings
                        st.success("✅ Embeddings listos")
        
        if st.button("🚀 Consultar con Métricas") and query:
            if st.session_state.eval_rag['embeddings'] is None:
                st.warning("Genera embeddings primero")
            else:
                with st.spinner("Procesando con métricas..."):
                    results, retrieval_time = hybrid_search_with_metrics(
                        query, 
                        st.session_state.eval_rag['documents'],
                        st.session_state.eval_rag['embeddings'],
                        client,
                        top_k
                    )
                    
                    response, generation_time = generate_response_with_metrics(client, query, results)
                    
                    metrics = {
                        'retrieval_time': retrieval_time,
                        'generation_time': generation_time,
                        'total_time': retrieval_time + generation_time,
                        'docs_retrieved': len(results),
                        'avg_relevance_score': np.mean([r['combined_score'] for r in results])
                    }
                    
                    if eval_enabled:
                        context_text = "\n".join([r['document'] for r in results])
                        
                        with st.spinner("Evaluando calidad..."):
                            metrics['faithfulness'] = evaluate_faithfulness(client, query, context_text, response)
                            metrics['relevance'] = evaluate_relevance(client, query, response)
                            metrics['context_precision'] = evaluate_context_precision(client, query, results)
                    
                    st.subheader("📋 Documentos Recuperados")
                    for i, result in enumerate(results):
                        with st.expander(f"Doc {i+1} - Score: {result['combined_score']:.3f}"):
                            st.write(result['document'])
                    
                    st.subheader("🤖 Respuesta")
                    st.write(response)
                    
                    st.subheader("⏱️ Métricas de Rendimiento")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Tiempo total", f"{metrics['total_time']:.2f}s")
                    with col2:
                        st.metric("Recuperación", f"{metrics['retrieval_time']:.2f}s")
                    with col3:
                        st.metric("Generación", f"{metrics['generation_time']:.2f}s")
                    with col4:
                        st.metric("Docs recuperados", metrics['docs_retrieved'])
                    
                    if eval_enabled:
                        st.subheader("🎯 Métricas de Calidad")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Fidelidad", f"{metrics['faithfulness']:.1f}/10")
                        with col2:
                            st.metric("Relevancia", f"{metrics['relevance']:.1f}/10")
                        with col3:
                            st.metric("Precisión contexto", f"{metrics['context_precision']:.2f}")
                    
                    if st.session_state.eval_rag['enable_logging']:
                        log_interaction(query, response, metrics, results)
    
    with tab2:
        st.header("📊 Dashboard de Métricas")
        
        if st.session_state.interaction_logs:
            df = pd.DataFrame([
                {
                    'timestamp': log['timestamp'],
                    'query_length': len(log['query']),
                    'response_length': len(log['response']),
                    **log['metrics']
                }
                for log in st.session_state.interaction_logs
            ])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Tiempo de Respuesta")
                fig = px.line(df, x='timestamp', y='total_time', title="Tiempo Total por Consulta")
                st.plotly_chart(fig, use_container_width=True)
                
                if 'faithfulness' in df.columns:
                    st.subheader("Distribución de Fidelidad")
                    fig = px.histogram(df, x='faithfulness', title="Distribución Scores Fidelidad")
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Métricas de Recuperación")
                fig = px.scatter(df, x='retrieval_time', y='generation_time', 
                               size='docs_retrieved', title="Tiempo Recuperación vs Generación")
                st.plotly_chart(fig, use_container_width=True)
                
                if 'relevance' in df.columns and 'context_precision' in df.columns:
                    st.subheader("Calidad vs Precisión")
                    fig = px.scatter(df, x='context_precision', y='relevance', 
                                   title="Precisión Contexto vs Relevancia")
                    st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📈 Estadísticas Generales")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total consultas", len(df))
            with col2:
                st.metric("Tiempo promedio", f"{df['total_time'].mean():.2f}s")
            with col3:
                if 'faithfulness' in df.columns:
                    st.metric("Fidelidad promedio", f"{df['faithfulness'].mean():.1f}/10")
            with col4:
                if 'relevance' in df.columns:
                    st.metric("Relevancia promedio", f"{df['relevance'].mean():.1f}/10")
        else:
            st.info("No hay datos de interacciones aún. Realiza algunas consultas primero.")
    
    with tab3:
        st.header("🧪 Evaluación Sistemática")
        
        if st.button("🧪 Ejecutar Evaluación Completa"):
            if st.session_state.eval_rag['embeddings'] is None:
                st.warning("Genera embeddings primero")
            else:
                eval_dataset = create_evaluation_dataset()
                results = []
                
                with st.spinner("Ejecutando evaluación sistemática..."):
                    for test_case in eval_dataset:
                        query = test_case['query']
                        
                        docs, retrieval_time = hybrid_search_with_metrics(
                            query,
                            st.session_state.eval_rag['documents'],
                            st.session_state.eval_rag['embeddings'],
                            client,
                            3
                        )
                        
                        response, generation_time = generate_response_with_metrics(client, query, docs)
                        
                        context_text = "\n".join([d['document'] for d in docs])
                        faithfulness = evaluate_faithfulness(client, query, context_text, response)
                        relevance = evaluate_relevance(client, query, response)
                        context_precision = evaluate_context_precision(client, query, docs)
                        
                        results.append({
                            'query': query,
                            'response': response,
                            'retrieval_time': retrieval_time,
                            'generation_time': generation_time,
                            'faithfulness': faithfulness,
                            'relevance': relevance,
                            'context_precision': context_precision,
                            'ground_truth': test_case['ground_truth']
                        })
                
                st.subheader("📊 Resultados de Evaluación")
                eval_df = pd.DataFrame(results)
                st.dataframe(eval_df)
                
                st.subheader("📈 Métricas Promedio")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Fidelidad", f"{eval_df['faithfulness'].mean():.1f}/10")
                with col2:
                    st.metric("Relevancia", f"{eval_df['relevance'].mean():.1f}/10")
                with col3:
                    st.metric("Precisión", f"{eval_df['context_precision'].mean():.2f}")
                with col4:
                    st.metric("Tiempo total", f"{(eval_df['retrieval_time'] + eval_df['generation_time']).mean():.2f}s")
    
    with tab4:
        st.header("📈 Analytics y Exportación")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📤 Exportar Datos")
            
            if st.button("📊 Exportar para LangSmith"):
                if st.session_state.interaction_logs:
                    langsmith_data = export_langsmith_format(st.session_state.interaction_logs)
                    st.json(langsmith_data[:2])
                    
                    json_str = json.dumps(langsmith_data, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="💾 Descargar JSON LangSmith",
                        data=json_str,
                        file_name=f"langsmith_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                else:
                    st.info("No hay datos para exportar")
            
            if st.button("📊 Exportar CSV"):
                if st.session_state.interaction_logs:
                    df = pd.DataFrame([
                        {
                            'timestamp': log['timestamp'],
                            'query': log['query'],
                            'response': log['response'][:100] + "...",
                            **log['metrics']
                        }
                        for log in st.session_state.interaction_logs
                    ])
                    
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="💾 Descargar CSV",
                        data=csv,
                        file_name=f"rag_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
        
        with col2:
            st.subheader("🔧 Gestión de Datos")
            
            if st.button("🗑️ Limpiar Logs"):
                st.session_state.interaction_logs = []
                st.success("Logs limpiados")
            
            uploaded_file = st.file_uploader("📥 Importar logs JSON", type=['json'])
            if uploaded_file:
                try:
                    imported_data = json.load(uploaded_file)
                    st.session_state.interaction_logs.extend(imported_data)
                    st.success(f"Importados {len(imported_data)} registros")
                except:
                    st.error("Error al importar archivo")
        
        st.subheader("ℹ️ Integración con Plataformas")
        with st.expander("Información de integración"):
            st.write("""
            **🔧 LangSmith Integration:**
            - Exporta métricas en formato compatible
            - Incluye run_ids únicos para trazabilidad
            - Métricas de tiempo y calidad
            
            **📊 Langfuse Integration:**
            - Formato JSON estructurado
            - Metadatos de contexto y scores
            - Timestamps para análisis temporal
            
            **📈 Arize Integration:**
            - Métricas de rendimiento
            - Datos de entrada y salida
            - Scores de evaluación automática
            """)

if __name__ == "__main__":
    main()