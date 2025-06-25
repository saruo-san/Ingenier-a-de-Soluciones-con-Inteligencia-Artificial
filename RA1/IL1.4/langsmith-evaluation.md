# Evaluación de Sistemas RAG con LangSmith

## 📋 Introducción

LangSmith es una plataforma de observabilidad y evaluación desarrollada por LangChain para monitorear, debuggear y evaluar aplicaciones basadas en modelos de lenguaje. Es especialmente útil para sistemas RAG (Retrieval-Augmented Generation) donde necesitamos evaluar tanto la recuperación de información como la generación de respuestas.

## 🎯 ¿Qué es LangSmith?

LangSmith proporciona:
- **Trazabilidad completa**: Seguimiento detallado de cada paso en tu pipeline RAG
- **Evaluaciones automáticas**: Métricas predefinidas y personalizadas
- **Datasets de evaluación**: Gestión de casos de prueba y ground truth
- **Debugging visual**: Interfaz para entender qué está pasando en cada paso
- **Comparación de modelos**: Análisis lado a lado de diferentes configuraciones

## 🚀 Configuración Inicial

### 1. Instalación

```bash
pip install langsmith langchain
```

### 2. Configuración de API Keys

```python
import os
from langsmith import Client

# Configurar variables de entorno
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "tu_api_key_aqui"
os.environ["LANGCHAIN_PROJECT"] = "rag-evaluation-project"

# Inicializar cliente
client = Client()
```

### 3. Obtener API Key

1. Ir a [smith.langchain.com](https://smith.langchain.com)
2. Crear cuenta o iniciar sesión
3. Navegar a Settings → API Keys
4. Crear nueva API key
5. Copiar y guardar de forma segura

## 📊 Configuración Básica para RAG

### 1. Instrumentar tu Sistema RAG

```python
from langchain.schema import Document
from langchain.callbacks import LangChainTracer
from langsmith import traceable

@traceable(name="retrieval_step")
def retrieve_documents(query: str, top_k: int = 5):
    """Función de recuperación instrumentada"""
    # Tu lógica de recuperación aquí
    documents = search_vector_db(query, top_k)
    
    # LangSmith automáticamente captura inputs/outputs
    return documents

@traceable(name="generation_step") 
def generate_response(query: str, context: str):
    """Función de generación instrumentada"""
    prompt = f"Contexto: {context}\nPregunta: {query}\nRespuesta:"
    
    response = llm.invoke(prompt)
    return response

@traceable(name="rag_pipeline")
def rag_pipeline(query: str):
    """Pipeline RAG completo"""
    # Paso 1: Recuperación
    documents = retrieve_documents(query)
    
    # Paso 2: Preparar contexto
    context = "\n".join([doc.page_content for doc in documents])
    
    # Paso 3: Generación
    response = generate_response(query, context)
    
    return {
        "query": query,
        "retrieved_docs": documents,
        "context": context,
        "response": response
    }
```

### 2. Ejemplo con LangChain

```python
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI

# Configurar componentes
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_texts(texts, embeddings)
llm = OpenAI(temperature=0)

# Crear chain con trazabilidad automática
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Ejecutar con trazabilidad
result = qa_chain({"query": "¿Qué es la inteligencia artificial?"})
```

## 🧪 Evaluaciones con LangSmith

### 1. Crear Dataset de Evaluación

```python
from langsmith import Client

client = Client()

# Crear dataset
dataset_name = "rag-evaluation-dataset"
dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="Dataset para evaluar sistema RAG"
)

# Agregar ejemplos al dataset
examples = [
    {
        "inputs": {"query": "¿Qué es la inteligencia artificial?"},
        "outputs": {"answer": "La IA es una rama de la informática..."},
        "metadata": {"category": "definiciones", "difficulty": "basic"}
    },
    {
        "inputs": {"query": "¿Cómo funciona el machine learning?"},
        "outputs": {"answer": "El ML utiliza algoritmos que aprenden..."},
        "metadata": {"category": "conceptos", "difficulty": "intermediate"}
    }
]

for example in examples:
    client.create_example(
        dataset_id=dataset.id,
        inputs=example["inputs"],
        outputs=example["outputs"],
        metadata=example["metadata"]
    )
```

### 2. Ejecutar Evaluaciones

```python
from langsmith.evaluation import evaluate, LangChainStringEvaluator

# Definir evaluadores
evaluators = [
    # Evaluador de relevancia
    LangChainStringEvaluator(
        "labeled_score_string",
        config={
            "criteria": {
                "relevance": "¿Qué tan relevante es la respuesta para la pregunta?"
            },
            "normalize_by": 10
        }
    ),
    
    # Evaluador de fidelidad
    LangChainStringEvaluator(
        "labeled_score_string", 
        config={
            "criteria": {
                "faithfulness": "¿La respuesta está basada en el contexto proporcionado?"
            },
            "normalize_by": 10
        }
    )
]

# Ejecutar evaluación
def rag_predict(inputs):
    """Función que será evaluada"""
    query = inputs["query"]
    result = rag_pipeline(query)
    return {"answer": result["response"]}

# Correr evaluación
results = evaluate(
    rag_predict,
    data=dataset_name,
    evaluators=evaluators,
    experiment_prefix="rag-v1",
    metadata={"version": "1.0", "model": "gpt-4"}
)

print(f"Resultados: {results}")
```

### 3. Evaluadores Personalizados

```python
from langsmith.schemas import Run, Example

def custom_context_precision_evaluator(run: Run, example: Example) -> dict:
    """Evaluador personalizado para precisión del contexto"""
    
    # Obtener documentos recuperados de la traza
    retrieved_docs = []
    for child_run in run.child_runs:
        if child_run.name == "retrieval_step":
            retrieved_docs = child_run.outputs.get("documents", [])
    
    query = run.inputs["query"]
    
    # Evaluar relevancia de cada documento
    relevant_count = 0
    for doc in retrieved_docs:
        # Lógica para determinar si el documento es relevante
        relevance_score = evaluate_document_relevance(query, doc)
        if relevance_score > 0.7:
            relevant_count += 1
    
    precision = relevant_count / len(retrieved_docs) if retrieved_docs else 0
    
    return {
        "score": precision,
        "value": precision,
        "comment": f"Documentos relevantes: {relevant_count}/{len(retrieved_docs)}"
    }

# Usar evaluador personalizado
results = evaluate(
    rag_predict,
    data=dataset_name,
    evaluators=[custom_context_precision_evaluator],
    experiment_prefix="rag-context-precision"
)
```

## 📈 Métricas Clave para RAG

### 1. Métricas de Recuperación

```python
# Context Precision: ¿Los documentos recuperados son relevantes?
def context_precision(retrieved_docs, query):
    relevant_docs = [doc for doc in retrieved_docs if is_relevant(doc, query)]
    return len(relevant_docs) / len(retrieved_docs)

# Context Recall: ¿Se recuperaron todos los documentos relevantes?
def context_recall(retrieved_docs, all_relevant_docs):
    retrieved_relevant = set(retrieved_docs) & set(all_relevant_docs)
    return len(retrieved_relevant) / len(all_relevant_docs)
```

### 2. Métricas de Generación

```python
# Faithfulness: ¿La respuesta es fiel al contexto?
def faithfulness_evaluator(context, response):
    prompt = f"""
    Contexto: {context}
    Respuesta: {response}
    
    ¿La respuesta está completamente basada en el contexto? (Sí/No)
    """
    # Evaluar con LLM
    
# Relevance: ¿La respuesta es relevante para la pregunta?
def relevance_evaluator(query, response):
    prompt = f"""
    Pregunta: {query}
    Respuesta: {response}
    
    Califica la relevancia de 1-10:
    """
    # Evaluar con LLM
```

### 3. Configuración de Evaluación Completa

```python
def comprehensive_rag_evaluation():
    """Evaluación completa del sistema RAG"""
    
    evaluators = [
        # Métricas automáticas
        LangChainStringEvaluator("labeled_score_string", config={
            "criteria": {"relevance": "Relevancia de la respuesta"},
            "normalize_by": 10
        }),
        
        LangChainStringEvaluator("labeled_score_string", config={
            "criteria": {"faithfulness": "Fidelidad al contexto"},
            "normalize_by": 10
        }),
        
        LangChainStringEvaluator("labeled_score_string", config={
            "criteria": {"completeness": "Completitud de la respuesta"},
            "normalize_by": 10
        }),
        
        # Evaluadores personalizados
        custom_context_precision_evaluator,
        response_length_evaluator,
        semantic_similarity_evaluator
    ]
    
    results = evaluate(
        rag_predict,
        data="rag-comprehensive-dataset",
        evaluators=evaluators,
        experiment_prefix="rag-comprehensive",
        metadata={
            "model": "gpt-4",
            "retrieval_method": "semantic_search",
            "chunk_size": 500,
            "top_k": 5
        }
    )
    
    return results
```

## 🔍 Análisis de Resultados

### 1. Dashboard de LangSmith

Accede a [smith.langchain.com](https://smith.langchain.com) para ver:

- **Experiments**: Comparar diferentes configuraciones
- **Datasets**: Gestionar casos de prueba
- **Traces**: Explorar ejecuciones individuales
- **Analytics**: Métricas agregadas y tendencias

### 2. Análisis Programático

```python
# Obtener resultados de experimento
experiment_results = client.list_runs(
    project_name="rag-evaluation-project",
    execution_order=1,
    is_root=True
)

# Analizar métricas
scores = []
for run in experiment_results:
    if run.feedback_stats:
        scores.append(run.feedback_stats)

# Calcular estadísticas
import numpy as np
avg_relevance = np.mean([s.get('relevance', 0) for s in scores])
avg_faithfulness = np.mean([s.get('faithfulness', 0) for s in scores])

print(f"Relevancia promedio: {avg_relevance:.2f}")
print(f"Fidelidad promedio: {avg_faithfulness:.2f}")
```

### 3. Exportar Datos

```python
# Exportar resultados para análisis externo
import pandas as pd

def export_evaluation_results(project_name, output_file):
    """Exporta resultados de evaluación a CSV"""
    
    runs = client.list_runs(project_name=project_name)
    
    data = []
    for run in runs:
        data.append({
            'run_id': run.id,
            'query': run.inputs.get('query', ''),
            'response': run.outputs.get('answer', ''),
            'latency': run.latency,
            'total_tokens': run.total_tokens,
            'feedback': run.feedback_stats
        })
    
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Resultados exportados a {output_file}")

export_evaluation_results("rag-evaluation-project", "rag_results.csv")
```

## 🔧 Mejores Prácticas

### 1. Diseño de Datasets

- **Diversidad**: Incluir diferentes tipos de consultas
- **Ground Truth**: Respuestas de referencia bien definidas
- **Metadatos**: Categorías, dificultad, dominio
- **Tamaño**: Balance entre cobertura y tiempo de evaluación

### 2. Configuración de Evaluadores

- **Múltiples Métricas**: No depender de una sola métrica
- **Evaluadores Humanos**: Combinar con evaluación automática
- **Contexto Específico**: Adaptar criterios al dominio
- **Calibración**: Validar evaluadores con ejemplos conocidos

### 3. Monitoreo Continuo

```python
# Configurar alertas automáticas
def setup_monitoring():
    """Configurar monitoreo continuo"""
    
    # Evaluación en producción
    @traceable(name="production_rag")
    def production_rag_with_monitoring(query):
        result = rag_pipeline(query)
        
        # Evaluación rápida en línea
        quick_score = quick_relevance_check(query, result["response"])
        
        # Log si la puntuación es baja
        if quick_score < 0.5:
            print(f"⚠️  Baja puntuación detectada: {quick_score}")
        
        return result
    
    return production_rag_with_monitoring
```

### 4. Versionado y Experimentos

```python
# Configuración de experimentos A/B
experiment_configs = {
    "baseline": {
        "chunk_size": 500,
        "top_k": 3,
        "model": "gpt-3.5-turbo"
    },
    "optimized": {
        "chunk_size": 300,
        "top_k": 5,
        "model": "gpt-4"
    }
}

for config_name, config in experiment_configs.items():
    results = evaluate(
        lambda inputs: rag_predict_with_config(inputs, config),
        data="standard-dataset",
        evaluators=standard_evaluators,
        experiment_prefix=f"rag-{config_name}",
        metadata=config
    )
```

## 🎓 Casos de Uso Avanzados

### 1. Evaluación Multi-Modal

```python
# Para RAG que maneja texto e imágenes
def multimodal_rag_evaluator(run, example):
    """Evaluador para RAG multi-modal"""
    
    query = run.inputs["query"]
    response = run.outputs["answer"]
    images = run.inputs.get("images", [])
    
    # Evaluar coherencia entre texto e imágenes
    coherence_score = evaluate_text_image_coherence(response, images)
    
    return {"score": coherence_score}
```

### 2. Evaluación de Dominio Específico

```python
# Para RAG médico, legal, técnico, etc.
def domain_specific_evaluator(domain):
    """Crear evaluador específico del dominio"""
    
    def evaluator(run, example):
        response = run.outputs["answer"]
        
        # Verificar terminología específica del dominio
        terminology_score = check_domain_terminology(response, domain)
        
        # Verificar precisión factual
        factual_score = verify_domain_facts(response, domain)
        
        return {
            "terminology_score": terminology_score,
            "factual_accuracy": factual_score
        }
    
    return evaluator
```

## 📚 Recursos Adicionales

### Documentación Oficial
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangSmith Python SDK](https://python.langchain.com/docs/langsmith/)
- [Evaluation Guide](https://docs.smith.langchain.com/evaluation)

### Ejemplos de Código
- [LangSmith Cookbook](https://github.com/langchain-ai/langsmith-cookbook)
- [RAG Evaluation Examples](https://github.com/langchain-ai/rag-evaluation-examples)

### Comunidad
- [LangChain Discord](https://discord.gg/langchain)
- [GitHub Discussions](https://github.com/langchain-ai/langchain/discussions)

## 🎯 Conclusión

LangSmith proporciona una plataforma robusta para evaluar sistemas RAG de manera sistemática y escalable. La combinación de trazabilidad automática, evaluadores flexibles y análisis visual permite optimizar continuamente el rendimiento de tus aplicaciones de IA.

**Próximos pasos recomendados:**
1. Configurar LangSmith en tu proyecto RAG actual
2. Crear un dataset de evaluación representativo
3. Implementar evaluadores básicos (relevancia, fidelidad)
4. Establecer un pipeline de evaluación continua
5. Iterar y optimizar basándose en los resultados