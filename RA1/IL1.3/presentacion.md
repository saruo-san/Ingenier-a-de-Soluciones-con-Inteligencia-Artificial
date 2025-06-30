# Presentación IL1.3 - Diseño de Infraestructura RAG

## Slide 1: Título y Objetivos
**Título:** IL1.3 - Diseño de Infraestructura RAG  
**Subtítulo:** Retrieval-Augmented Generation - Arquitecturas de Solución Integrales

**Objetivos:**
- Diseñar arquitecturas RAG que integren LLMs y recuperación de información
- Implementar sistemas de búsqueda semántica con embeddings vectoriales
- Desarrollar técnicas avanzadas de búsqueda híbrida y re-ranking
- Establecer pipelines de evaluación y monitoreo de calidad
- Integrar herramientas de observabilidad para sistemas productivos

---

## Slide 2: ¿Qué es RAG?
**Título:** Fundamentos de Retrieval-Augmented Generation

**Definición:**
RAG combina la **búsqueda de información relevante** con la **generación de texto** para producir respuestas más precisas y contextualizadas.

**Problema que resuelve:**
- LLMs tienen conocimiento limitado a su fecha de entrenamiento
- Pueden "alucinar" información incorrecta
- No acceden a datos específicos de la organización

**Solución RAG:**
1. **Recuperar** documentos relevantes de una base de conocimiento
2. **Aumentar** el prompt con el contexto recuperado
3. **Generar** respuesta basada en información actual y específica

**Beneficios:**
- Respuestas más precisas y actualizadas
- Control sobre fuentes de información
- Reducción de alucinaciones
- Capacidad de citar fuentes

---

## Slide 3: Arquitectura General de RAG
**Título:** Componentes Principales del Sistema

**Pipeline básico:**
```
Consulta → Recuperación → Contexto → LLM → Respuesta
```

**Componentes clave:**
1. **Base de Conocimiento**
   - Documentos, chunks, metadatos
   - Almacenamiento vectorial y textual

2. **Sistema de Recuperación**
   - Embeddings y búsqueda semántica
   - Índices vectoriales eficientes

3. **Modelo de Lenguaje**
   - Generación contextualizada
   - Control de temperatura y tokens

4. **Orquestación**
   - Pipeline de procesamiento
   - Manejo de errores y fallbacks

**Consideraciones técnicas:**
- Precisión vs. velocidad
- Escalabilidad y latencia
- Control de calidad y relevancia

---

## Slide 4: RAG Básico - Implementación Inicial
**Título:** Script 1 - Basic RAG (1-basic-rag.py)

**Características:**
- Búsqueda simple por coincidencia de palabras clave
- Almacenamiento en memoria temporal
- Interfaz Streamlit para demostración
- Configuración básica con OpenAI client

**Componentes implementados:**
```python
def simple_retrieval(query, documents):
    # Búsqueda por palabras clave
    relevant_docs = []
    for doc in documents:
        if any(word in doc.lower() for word in query.lower().split()):
            relevant_docs.append(doc)
    return relevant_docs[:3]
```

**Casos de uso:**
- Prototipos rápidos
- Demostraciones conceptuales
- Validación de ideas básicas

**Limitaciones:**
- Búsqueda poco sofisticada
- Sin comprensión semántica
- Almacenamiento no persistente

---

## Slide 5: RAG con Vectores - Búsqueda Semántica
**Título:** Script 2 - Vector RAG (2-vector-rag.py)

**Mejoras implementadas:**
- **Embeddings semánticos** con text-embedding-3-small
- **Búsqueda por similitud coseno** para relevancia semántica
- **Chunking inteligente** para documentos largos
- **Carga de archivos** externos
- **Umbral de similitud** configurable

**Técnicas clave:**
```python
def get_embeddings(client, texts):
    # Generar embeddings semánticos
    embeddings = []
    for text in texts:
        response = client.embeddings.create(
            model="text-embedding-3-small", input=text)
        embeddings.append(response.data[0].embedding)
    return np.array(embeddings)

def vector_search(query_embedding, doc_embeddings, documents, top_k=3):
    # Búsqueda por similitud coseno
    similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]
    return results
```

**Ventajas:**
- Comprensión semántica real
- Mejor precisión en búsqueda
- Escalable a grandes corpus

---

## Slide 6: RAG Avanzado - Técnicas Sofisticadas
**Título:** Script 3 - Advanced RAG (3-advanced-rag.py)

**Funcionalidades avanzadas:**

1. **Búsqueda Híbrida**
   - Combina similitud semántica + coincidencia de palabras clave
   - Pesos configurables (70% semántico, 30% keywords)

2. **Re-ranking con LLM**
   - Segunda evaluación de relevancia por el modelo
   - Mejora precisión de documentos seleccionados

3. **Expansión de Consultas**
   - Genera variaciones semánticas de la consulta original
   - Búsqueda más amplia y completa

4. **Memoria Conversacional**
   - Mantiene historial de interacciones
   - Contexto persistente entre consultas

5. **Configuración Dinámica**
   - Parámetros ajustables en tiempo real
   - A/B testing de configuraciones

**Ejemplo de búsqueda híbrida:**
```python
def hybrid_search(query, documents, embeddings, client, top_k=5):
    # Combinar scores semánticos y keywords
    semantic_similarities = cosine_similarity([query_embedding], embeddings)[0]
    keyword_scores = calculate_keyword_overlap(query, documents)
    combined_scores = 0.7 * semantic_similarities + 0.3 * keyword_scores
    return top_results
```

---

## Slide 7: Técnicas de Re-ranking
**Título:** Mejorando la Precisión de Recuperación

**¿Por qué re-ranking?**
- Primera búsqueda puede no ser óptima
- LLM puede evaluar relevancia mejor que métricas simples
- Permite refinamiento contextual

**Implementación:**
```python
def rerank_results(client, query, results, top_k=3):
    rerank_prompt = f"""Evalúa qué tan relevante es cada documento para: "{query}"
    Asigna puntuación 0-10 donde 10 es extremadamente relevante.
    
    Documentos: [lista de documentos]
    Responde SOLO con números separados por comas: """
    
    # Obtener scores del LLM y reordenar
    scores = get_llm_scores(rerank_prompt)
    return sorted_results_by_llm_scores
```

**Beneficios:**
- Mejora significativa en precisión
- Contexto más relevante para generación
- Adaptable a diferentes dominios

**Consideraciones:**
- Mayor latencia por llamadas adicionales al LLM
- Costo adicional en tokens
- Balance entre precisión y velocidad

---

## Slide 8: Expansión de Consultas
**Título:** Ampliando el Espacio de Búsqueda

**Concepto:**
Generar múltiples variaciones de la consulta original para capturar información relacionada que podría no encontrarse con la consulta exacta.

**Implementación:**
```python
def query_expansion(client, query):
    expansion_prompt = f"""Dado esta consulta: "{query}"
    
    Genera 3 consultas relacionadas que podrían ayudar a encontrar 
    información complementaria. Las consultas deben ser variaciones 
    semánticas o aspectos relacionados."""
    
    # Buscar con consulta original + variaciones
    expanded_queries = generate_variations(query)
    all_results = []
    for q in expanded_queries:
        results = search(q)
        all_results.extend(results)
    
    return deduplicate_and_rank(all_results)
```

**Ventajas:**
- Cobertura más amplia de información relevante
- Captura aspectos no explícitos en consulta original
- Mejora recall sin sacrificar precisión

---

## Slide 9: Evaluación y Monitoreo de RAG
**Título:** Script 4 - Evaluation RAG (4-evaluation-rag.py)

**Métricas implementadas:**

1. **Métricas de Rendimiento**
   - Tiempo de recuperación
   - Tiempo de generación
   - Throughput del sistema

2. **Métricas de Calidad**
   - **Faithfulness:** ¿La respuesta es fiel al contexto?
   - **Relevance:** ¿La respuesta es relevante a la consulta?
   - **Context Precision:** ¿Los documentos recuperados son relevantes?

3. **Evaluación Automática**
```python
def evaluate_faithfulness(client, query, context, response):
    eval_prompt = f"""¿La respuesta está basada únicamente en el contexto?
    Consulta: {query}
    Contexto: {context}
    Respuesta: {response}
    
    Responde con número 1-10 donde:
    1-3: No basada en contexto
    7-10: Completamente fiel al contexto"""
    return llm_score
```

**Dashboard de métricas:**
- Visualizaciones en tiempo real
- Trends temporales
- Alertas por degradación

---

## Slide 10: Logging y Observabilidad
**Título:** Monitoreo en Producción

**Logging estructurado:**
```python
def log_interaction(query, response, metrics, context_docs):
    log_entry = {
        'id': str(uuid.uuid4()),
        'timestamp': datetime.now().isoformat(),
        'query': query,
        'response': response,
        'metrics': metrics,
        'context_count': len(context_docs),
        'context_scores': [doc.get('combined_score', 0) for doc in context_docs]
    }
    session_state.interaction_logs.append(log_entry)
```

**Integración con plataformas:**
- **LangSmith:** Trazabilidad completa de ejecuciones
- **Langfuse:** Analytics y debugging de prompts
- **Arize:** Monitoreo de ML performance

**Métricas clave para producción:**
- Latencia p95, p99
- Tasa de respuestas satisfactorias
- Distribution de scores de calidad
- Volumen y patrones de uso

---

## Slide 11: Arquitectura de Datos
**Título:** Gestión de Conocimiento y Vectores

**Componentes de almacenamiento:**
1. **Base de documentos original**
   - Textos completos, metadatos
   - Versionado y actualización

2. **Índice vectorial**
   - Embeddings optimizados para búsqueda
   - Estructuras como FAISS, Pinecone, Weaviate

3. **Cache de resultados**
   - Consultas frecuentes
   - Reducción de latencia

**Estrategias de chunking:**
```python
def chunking_text(text, chunk_size=200, overlap=50):
    # División inteligente preservando contexto
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks
```

**Consideraciones:**
- Tamaño óptimo de chunks (100-500 tokens)
- Overlap para preservar contexto
- Metadata para filtros y routing

---

## Slide 12: Optimización de Performance
**Título:** Escalabilidad y Eficiencia

**Técnicas de optimización:**

1. **Búsqueda aproximada**
   - Algoritmos como HNSW para búsqueda rápida
   - Trade-off entre precisión y velocidad

2. **Caching inteligente**
   - Cache de embeddings frecuentes
   - Resultados de consultas similares

3. **Batch processing**
   - Procesamiento en lotes para eficiencia
   - Pipelines asíncronos

4. **Filtros pre-búsqueda**
   - Metadata filtering para reducir espacio de búsqueda
   - Filtros temporales, de categoría, etc.

**Métricas de performance:**
- QPS (Queries Per Second)
- Latencia media y percentiles
- Utilización de recursos (CPU/memoria)
- Costo por consulta

---

## Slide 13: Casos de Uso Empresariales
**Título:** Aplicaciones Prácticas de RAG

**Soporte al Cliente:**
- Base de conocimiento automatizada
- Respuestas consistentes 24/7
- Escalamiento sin aumentar personal

**Análisis de Documentos:**
- Procesamiento de contratos legales
- Análisis de informes financieros
- Due diligence automatizado

**Investigación y Desarrollo:**
- Búsqueda en literatura científica
- Análisis de patentes
- Síntesis de investigación

**Onboarding y Capacitación:**
- Manuales interactivos
- Q&A sobre políticas corporativas
- Entrenamiento personalizado

**Ventajas competitivas:**
- Conocimiento organizacional accesible
- Democratización de expertise
- Decisiones basadas en datos completos

---

## Slide 14: Integración con Herramientas de Observabilidad
**Título:** Monitoreo y Analytics Avanzados

**LangSmith Integration:**
```python
def export_langsmith_format(logs):
    return [{
        "run_id": log['id'],
        "timestamp": log['timestamp'],
        "inputs": {"query": log['query']},
        "outputs": {"response": log['response']},
        "metrics": log['metrics'],
        "metadata": {"context_count": log['context_count']}
    } for log in logs]
```

**Métricas de negocio:**
- Satisfacción del usuario
- Tiempo de resolución de consultas
- Reducción de escalaciones
- ROI del sistema RAG

**Alertas y monitoreo:**
- Degradación de calidad automática
- Anomalías en patrones de uso
- Performance thresholds
- Error rate monitoring

---

## Slide 15: Mejores Prácticas y Consideraciones
**Título:** Lessons Learned y Recomendaciones

**Diseño de sistema:**
1. **Empezar simple:** RAG básico → vectorial → avanzado
2. **Medir temprano:** Establecer métricas desde el inicio
3. **Iterar basado en datos:** User feedback + métricas
4. **Considerar costos:** Balance calidad vs. precio

**Calidad de datos:**
- Curación cuidadosa de documentos fuente
- Actualización regular de conocimiento
- Validación de embeddings
- Monitoreo de drift

**Experiencia de usuario:**
- Transparencia en fuentes citadas
- Indicación de confianza en respuestas
- Fallbacks para consultas no respondibles
- Feedback loop con usuarios

**Seguridad y privacidad:**
- Control de acceso a documentos sensibles
- Anonimización cuando necesario
- Audit trails completos
- Compliance con regulaciones

---

## Slide 16: Roadmap Tecnológico
**Título:** Evolución y Próximos Pasos

**Tendencias emergentes:**
- **Multimodal RAG:** Texto + imágenes + audio
- **Agentic RAG:** Sistemas que pueden hacer acciones
- **Federated RAG:** Búsqueda across multiple knowledge bases
- **Real-time RAG:** Actualización en tiempo real

**Próximos módulos:**
- **IL1.4:** Evaluación y optimización integral de sistemas LLM
- **RA2:** Desarrollo de agentes inteligentes
- **IL2.1:** Arquitectura de agentes y frameworks

**Habilidades desarrolladas:**
- Arquitectura de sistemas RAG completos
- Evaluación sistemática de calidad
- Integración con herramientas de observabilidad
- Optimización de performance y costos

---

## Slide 17: Resumen Ejecutivo
**Título:** Conceptos Clave del Módulo IL1.3

**Progresión técnica implementada:**
1. **RAG Básico:** Fundamentos y búsqueda simple
2. **RAG Vectorial:** Embeddings y búsqueda semántica
3. **RAG Avanzado:** Híbrido, re-ranking, expansión, memoria
4. **RAG con Evaluación:** Métricas, monitoreo, observabilidad

**Capacidades técnicas adquiridas:**
- Diseño de arquitecturas RAG escalables
- Implementación de búsqueda semántica avanzada
- Sistemas de evaluación automática
- Integración con plataformas de observabilidad
- Optimización de performance y calidad

**Impacto organizacional:**
- Democratización del conocimiento empresarial
- Automatización de consultas complejas
- Mejora en precisión de respuestas
- Escalabilidad de expertise humana
- Foundation para sistemas de agentes inteligentes

**Preparación para producción:**
- Logging estructurado y métricas
- Monitoreo continuo de calidad
- Estrategias de optimización
- Integración con herramientas enterprise