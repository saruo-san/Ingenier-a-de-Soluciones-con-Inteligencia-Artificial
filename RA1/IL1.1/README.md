# IL1.1 - Introducción a LLMs y Conexiones API

## Introducción

Esta unidad introduce los conceptos fundamentales de los Modelos de Lenguaje Grandes (LLMs) y las técnicas para establecer conexiones API efectivas. Aprenderás a interactuar con diferentes proveedores de LLMs y comprender las bases técnicas para el desarrollo de aplicaciones con IA generativa.

## Videos de cada archivo del curso:

- Configuración de Github Marketplace Models [1-github_model_api.ipynb](https://github.com/davila7/Ingenier-a-de-Soluciones-con-Inteligencia-Artificial/blob/main/RA1/IL1.1/1-github_model_api.ipynb):
[![Preview del Video de YouTube](https://img.youtube.com/vi/oYvwSROBTl0/hqdefault.jpg)](https://www.youtube.com/watch?v=oYvwSROBTl0)

## Objetivos de Aprendizaje

Al completar esta unidad, serás capaz de:

1. **Comprender los fundamentos de los LLMs**: Arquitectura, funcionamiento y capacidades
2. **Establecer conexiones API**: Configurar y usar APIs de diferentes proveedores
3. **Implementar patrones básicos**: Llamadas síncronas, streaming y gestión de memoria
4. **Aplicar mejores prácticas**: Configuración segura, manejo de errores y optimización

## Contenido del Módulo

### 1. Fundamentos Teóricos
- Arquitectura de los Transformers
- Entrenamiento y fine-tuning de LLMs
- Conceptos de tokens, embeddings y atención
- Proveedores principales: OpenAI, GitHub Models, Anthropic, Google

### 2. Implementaciones Prácticas

#### Notebook 1: GitHub Models API
**Archivo**: `1-github_model_api.ipynb`
- Configuración de credenciales y entorno
- Conexión directa con OpenAI client
- Parámetros básicos: temperature, max_tokens
- Manejo de respuestas y errores

#### Notebook 2: LangChain Model API
**Archivo**: `2-langchain_model_api.ipynb`
- Introducción al framework LangChain
- Abstracción de modelos con ChatOpenAI
- Ventajas de usar frameworks vs API directa
- Compatibilidad entre proveedores

#### Notebook 3: LangChain Streaming
**Archivo**: `3-langchain_streaming.ipynb`
- Implementación de respuestas en tiempo real
- Ventajas del streaming para UX
- Manejo de chunks y buffer de datos
- Casos de uso para aplicaciones interactivas

#### Notebook 4: LangChain Memory
**Archivo**: `4-langchain_memory.ipynb`
- Sistemas de memoria conversacional
- ConversationBufferMemory
- Persistencia de contexto entre interacciones
- Limitaciones y consideraciones de memoria

### 3. Conceptos de Prompting
**Archivo**: `prompting.md`
- Estructura y componentes de un prompt efectivo
- Técnicas de ingeniería de prompts
- Patrones comunes y mejores prácticas

## Configuración del Entorno

### Variables de Entorno Requeridas

```bash
export GITHUB_BASE_URL="https://models.inference.ai.azure.com"
export GITHUB_TOKEN="tu_token_de_github"
export OPENAI_BASE_URL="https://models.inference.ai.azure.com"
```

### Dependencias

```bash
pip install openai langchain langchain-openai
```

## Arquitectura Técnica

### Patrón de Conexión API

```python
# Configuración estándar
from openai import OpenAI

client = OpenAI(
    base_url=os.environ.get("GITHUB_BASE_URL"),
    api_key=os.environ.get("GITHUB_TOKEN")
)
```

### Abstracción con LangChain

```python
# Framework approach
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("GITHUB_TOKEN"),
    model="gpt-4o"
)
```

## Consideraciones Técnicas

### Seguridad
- Nunca hardcodear API keys en el código
- Usar variables de entorno para credenciales
- Implementar rate limiting y error handling

### Performance
- Configurar timeouts apropiados
- Usar streaming para respuestas largas
- Optimizar el uso de tokens

### Escalabilidad
- Considerar patrones de retry y circuit breaker
- Implementar logging para debugging
- Planificar para múltiples proveedores

## Evaluación

Esta unidad incluye:
- **Quiz teórico** (8 preguntas) sobre fundamentos de LLMs
- **Práctica dirigida** con los notebooks proporcionados
- **Ejercicios de implementación** para reforzar conceptos

## Recursos Adicionales

- [Documentación OpenAI API](https://platform.openai.com/docs)
- [GitHub Models Documentation](https://docs.github.com/en/github-models)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [Transformer Architecture Paper](https://arxiv.org/abs/1706.03762)

## Próximos Pasos

Al completar IL1.1, estarás preparado para:
- **IL1.2**: Técnicas avanzadas de prompt engineering
- **IL1.3**: Implementación de sistemas RAG
- **IL1.4**: Evaluación y optimización de LLMs