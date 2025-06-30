# Presentación IL2.2 - Memoria y Herramientas Externas

## Slide 1: Título y Objetivos
**Título:** IL2.2 - Memoria y Herramientas Externas  
**Subtítulo:** Sistemas de Memoria para Agentes LLM y Protocolo MCP

**Objetivos:**
- Comprender diferentes tipos de sistemas de memoria para agentes
- Implementar memoria conversacional, de trabajo y persistente
- Integrar herramientas externas con agentes LLM
- Utilizar el protocolo MCP (Model Context Protocol)
- Diseñar agentes con capacidades de memoria avanzadas

---

## Slide 2: ¿Por qué Memoria en Agentes?
**Título:** La Importancia de la Memoria en Agentes LLM

**Problema sin memoria:**
- Los LLMs son stateless (sin estado)
- Cada interacción es independiente
- No pueden recordar contexto previo
- Limitados por el tamaño de contexto

**Beneficios de la memoria:**
- **Continuidad:** Mantener contexto entre interacciones
- **Aprendizaje:** Recordar patrones y preferencias
- **Personalización:** Adaptar respuestas basadas en historial
- **Eficiencia:** Evitar repetir información conocida

**Tipos de limitaciones sin memoria:**
```
Usuario: "Mi nombre es Ana"
LLM: "Hola Ana, ¿en qué puedo ayudarte?"

Usuario: "¿Cuál es mi nombre?" (nueva sesión)
LLM: "No tengo información sobre tu nombre"
```

**Con sistema de memoria:**
```
Usuario: "¿Cuál es mi nombre?"
Agente: "Tu nombre es Ana, lo mencionaste anteriormente"
```

---

## Slide 3: Tipos de Memoria en Agentes
**Título:** Taxonomía de Sistemas de Memoria

**1. Memoria de Trabajo (Working Memory):**
- Información temporal para la tarea actual
- Se limpia entre sesiones diferentes
- Equivale al "scratchpad" del agente
- **Ejemplo:** Variables temporales, cálculos intermedios

**2. Memoria Conversacional:**
- Historial de la conversación actual
- Mantiene contexto de intercambios recientes
- **Ejemplo:** Últimos 5-10 mensajes del chat

**3. Memoria Episódica:**
- Eventos y experiencias específicas
- Recuerdos con contexto temporal
- **Ejemplo:** "El usuario preguntó sobre Python el martes pasado"

**4. Memoria Semántica:**
- Conocimiento general y hechos
- Información del dominio específico
- **Ejemplo:** "El usuario prefiere ejemplos en Python"

**5. Memoria Procedimental:**
- Cómo hacer tareas específicas
- Patrones de comportamiento aprendidos
- **Ejemplo:** "Para este usuario, siempre incluir ejemplos de código"

---

## Slide 4: Implementación Básica de Memoria
**Título:** Script 1 - Memoria Conversacional Simple

**Concepto básico:**
Agente que recuerda el último mensaje recibido

**Implementación:**
```python
class ConversationalAgent:
    def __init__(self):
        self.last_message = None

    def respond(self, message):
        response = f"Recibí tu mensaje: '{message}'"
        if self.last_message:
            response += f". Anteriormente me dijiste: '{self.last_message}'"
        self.last_message = message
        return response
```

**Ventajas:**
- Implementación simple
- Mínimo uso de recursos
- Contexto inmediato disponible

**Limitaciones:**
- Solo recuerda un mensaje
- No hay persistencia entre sesiones
- No hay búsqueda o filtrado

---

## Slide 5: Sistema de Memoria Avanzado
**Título:** Script 1 - Sistema de Memoria Completo

**Arquitectura de MemoryItem:**
```python
@dataclass
class MemoryItem:
    content: str           # Contenido de la memoria
    timestamp: float       # Cuándo se creó
    memory_type: str      # Tipo de memoria
    importance: float     # Nivel de importancia
    metadata: Dict        # Información adicional
```

**Sistema de Memoria Base:**
- **store():** Almacenar nueva memoria
- **retrieve():** Buscar memorias relevantes
- **clear():** Limpiar todas las memorias
- **get_stats():** Estadísticas del sistema

**Características avanzadas:**
- Límite máximo de memorias (evita overflow)
- Búsqueda por relevancia y importancia
- Metadata flexible para contexto adicional
- Estadísticas de uso y rendimiento

---

## Slide 6: Algoritmos de Recuperación de Memoria
**Título:** Estrategias para Encontrar Memorias Relevantes

**1. Búsqueda por Palabras Clave:**
```python
def retrieve(self, query: str, limit: int = 5):
    query_words = query.lower().split()
    for memory in self.memories:
        relevance = sum(1 for word in query_words 
                       if word in memory.content.lower())
```

**2. Búsqueda por Similitud Semántica:**
```python
# Usando embeddings vectoriales
def semantic_search(self, query_embedding, memories):
    similarities = [cosine_similarity(query_embedding, m.embedding) 
                   for m in memories]
    return sorted(memories, key=similarities, reverse=True)
```

**3. Búsqueda Temporal:**
```python
def recent_memories(self, hours=24):
    cutoff = time.time() - (hours * 3600)
    return [m for m in self.memories if m.timestamp > cutoff]
```

**4. Búsqueda por Importancia:**
```python
def important_memories(self, threshold=0.7):
    return [m for m in self.memories if m.importance > threshold]
```

---

## Slide 7: Herramientas Externas para Agentes
**Título:** Script 2 - Expandiendo Capacidades con Herramientas

**¿Qué son las herramientas externas?**
Funciones que permiten al agente interactuar más allá del texto:
- APIs web y servicios
- Bases de datos
- Sistemas de archivos
- Cálculos y procesamiento
- Comunicación (email, chat)

**Ejemplo básico:**
```python
def get_weather(city):
    """Simula obtener el clima de una ciudad"""
    return f"El clima en {city} es soleado"

class ToolAgent:
    def ask_weather(self, city):
        return get_weather(city)
```

**Beneficios:**
- Acceso a información en tiempo real
- Capacidades más allá del LLM
- Automatización de tareas complejas
- Integración con sistemas existentes

---

## Slide 8: Categorías de Herramientas Externas
**Título:** Tipos de Herramientas para Agentes

**1. Herramientas de Información:**
- Búsqueda web (Google, DuckDuckGo)
- APIs de datos (clima, noticias, finanzas)
- Bases de datos y knowledge bases
- Wikipedia y enciclopedias

**2. Herramientas de Computación:**
- Calculadora matemática
- Análisis estadístico
- Procesamiento de datos
- Compiladores y ejecutores de código

**3. Herramientas de Comunicación:**
- Email y mensajería
- APIs de redes sociales
- Webhooks y notificaciones
- Sistemas de tickets

**4. Herramientas de Almacenamiento:**
- Sistemas de archivos
- Bases de datos SQL/NoSQL
- Cloud storage (S3, Drive)
- Version control (Git)

**5. Herramientas de Automatización:**
- APIs REST/GraphQL
- RPA (Robotic Process Automation)
- Workflow engines
- Scheduling systems

---

## Slide 9: Protocolo MCP - Introducción
**Título:** Model Context Protocol - Conexión Segura con Recursos

**¿Qué es MCP?**
Protocolo estándar para que los LLMs accedan de forma segura a recursos externos:
- **Seguridad:** Conexiones autenticadas y autorizadas
- **Estandarización:** Protocolo común para diferentes herramientas
- **Escalabilidad:** Manejo eficiente de múltiples recursos
- **Observabilidad:** Logging y monitoreo de accesos

**Componentes del MCP:**
- **MCP Server:** Expone recursos y herramientas
- **MCP Client:** Conecta agentes con servidores
- **Resources:** Archivos, web pages, databases
- **Tools:** Funciones que pueden ejecutar acciones

**Ventajas vs conexión directa:**
- Autenticación centralizada
- Rate limiting automático
- Caching inteligente
- Error handling robusto

---

## Slide 10: Arquitectura del Protocolo MCP
**Título:** Componentes y Flujo de MCP

**Arquitectura típica:**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   LLM/Agent │◄──►│ MCP Client  │◄──►│ MCP Server  │
└─────────────┘    └─────────────┘    └─────────────┘
                                             │
                                             ▼
                                    ┌─────────────┐
                                    │  Resources  │
                                    │ (Files, DB, │
                                    │  APIs, etc) │
                                    └─────────────┘
```

**Flujo de operación:**
1. **Agente** solicita recurso o herramienta
2. **MCP Client** valida y formatea solicitud
3. **MCP Server** autentica y autoriza
4. **Resource** procesa la operación
5. **Resultado** se devuelve por la cadena

**Beneficios de esta arquitectura:**
- Separación de responsabilidades
- Reutilización de servidores MCP
- Security boundaries claros
- Monitoreo centralizado

---

## Slide 11: Tipos de Recursos MCP
**Título:** Recursos Disponibles a través de MCP

**1. File System Resources:**
```python
# Acceder a archivos locales de forma segura
mcp_client.read_file("/path/to/document.txt")
mcp_client.list_directory("/project/folder")
mcp_client.write_file("/output/result.json", data)
```

**2. Database Resources:**
```python
# Conectar con bases de datos
mcp_client.query_database("SELECT * FROM users WHERE active=1")
mcp_client.execute_procedure("update_user_status", user_id=123)
```

**3. Web Resources:**
```python
# Acceder a contenido web
mcp_client.fetch_webpage("https://api.example.com/data")
mcp_client.scrape_content("https://news.example.com", selector=".article")
```

**4. API Resources:**
```python
# Integrar con APIs externas
mcp_client.call_api("weather", city="Madrid")
mcp_client.call_api("translate", text="Hello", target_lang="es")
```

**Características de seguridad:**
- Sandboxing de operaciones
- Validación de permisos por recurso
- Audit trail completo
- Rate limiting por cliente

---

## Slide 12: Implementación de MCP Server
**Título:** Creando Servidores MCP Personalizados

**Estructura básica de MCP Server:**
```python
class MCPServer:
    def __init__(self, name: str):
        self.name = name
        self.resources = {}
        self.tools = {}
        self.permissions = {}
    
    def register_resource(self, name: str, resource):
        """Registrar recurso disponible"""
        self.resources[name] = resource
    
    def register_tool(self, name: str, func, description: str):
        """Registrar herramienta ejecutable"""
        self.tools[name] = {
            'function': func,
            'description': description
        }
    
    def handle_request(self, client_id: str, request: dict):
        """Procesar solicitud de cliente"""
        if not self.check_permissions(client_id, request):
            return {"error": "Unauthorized"}
        
        return self.execute_request(request)
```

**Ejemplo de recurso personalizado:**
```python
class WeatherResource:
    def get_weather(self, city: str) -> dict:
        # Integración con API real de clima
        return {
            "city": city,
            "temperature": 25,
            "condition": "sunny"
        }

# Registrar en servidor MCP
server.register_resource("weather", WeatherResource())
```

---

## Slide 13: MCP Client para Agentes
**Título:** Conectando Agentes con Recursos MCP

**Cliente MCP básico:**
```python
class MCPClient:
    def __init__(self, server_url: str, api_key: str):
        self.server_url = server_url
        self.api_key = api_key
        self.session = self.authenticate()
    
    def authenticate(self):
        """Autenticar con servidor MCP"""
        # Proceso de autenticación
        return session_token
    
    def request_resource(self, resource_name: str, action: str, **params):
        """Solicitar acceso a recurso"""
        request = {
            "resource": resource_name,
            "action": action,
            "parameters": params,
            "client_id": self.client_id
        }
        return self.send_request(request)
    
    def use_tool(self, tool_name: str, **params):
        """Ejecutar herramienta en servidor"""
        return self.request_resource("tools", "execute", 
                                   tool=tool_name, **params)
```

**Integración con agente:**
```python
class MCPEnabledAgent:
    def __init__(self, mcp_client):
        self.mcp = mcp_client
        self.memory = MemorySystem()
    
    def process_query(self, query: str):
        # Usar MCP para obtener información
        weather_data = self.mcp.use_tool("weather", city="Madrid")
        
        # Almacenar en memoria
        self.memory.store(f"Weather query: {weather_data}")
        
        return f"Weather in Madrid: {weather_data['condition']}"
```

---

## Slide 14: Patrones de Memoria Avanzados
**Título:** Estrategias Sofisticadas de Gestión de Memoria

**1. Memoria Jerárquica:**
```python
class HierarchicalMemory:
    def __init__(self):
        self.short_term = []     # Últimas interacciones  
        self.medium_term = []    # Sesión actual
        self.long_term = []      # Conocimiento persistente
    
    def consolidate(self):
        """Mover memorias importantes a long-term"""
        important = [m for m in self.medium_term if m.importance > 0.8]
        self.long_term.extend(important)
```

**2. Memoria con Decay (Olvido):**
```python
def apply_decay(self, memory: MemoryItem) -> float:
    """Reducir importancia con el tiempo"""
    age_hours = (time.time() - memory.timestamp) / 3600
    decay_factor = math.exp(-age_hours / 24)  # Half-life de 24h
    return memory.importance * decay_factor
```

**3. Memoria Asociativa:**
```python
class AssociativeMemory:
    def __init__(self):
        self.associations = {}  # memory_id -> [related_memory_ids]
    
    def create_association(self, memory1_id, memory2_id, strength=1.0):
        """Crear asociación entre memorias"""
        if memory1_id not in self.associations:
            self.associations[memory1_id] = []
        self.associations[memory1_id].append((memory2_id, strength))
```

**4. Memoria Contextual:**
```python
def retrieve_by_context(self, current_context: dict, limit=5):
    """Recuperar memorias relevantes al contexto actual"""
    scored_memories = []
    for memory in self.memories:
        context_score = self.calculate_context_similarity(
            current_context, memory.metadata.get('context', {})
        )
        scored_memories.append((memory, context_score))
    
    return sorted(scored_memories, key=lambda x: x[1], reverse=True)[:limit]
```

---

## Slide 15: Persistencia de Memoria
**Título:** Mantener Memoria entre Sesiones

**Opciones de persistencia:**

**1. Archivo JSON:**
```python
def save_to_file(self, filename: str):
    """Guardar memorias en archivo JSON"""
    data = [asdict(memory) for memory in self.memories]
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def load_from_file(self, filename: str):
    """Cargar memorias desde archivo"""
    with open(filename, 'r') as f:
        data = json.load(f)
    self.memories = [MemoryItem(**item) for item in data]
```

**2. Base de Datos SQLite:**
```python
import sqlite3

class SQLiteMemorySystem(MemorySystem):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    def store(self, content: str, memory_type: str = "general"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO memories (content, memory_type, timestamp)
            VALUES (?, ?, ?)
        """, (content, memory_type, time.time()))
        conn.commit()
        conn.close()
```

**3. Vector Database (para búsqueda semántica):**
```python
class VectorMemorySystem:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vector_db = ChromaDB()  # o Pinecone, Weaviate, etc.
    
    def store(self, content: str):
        embedding = self.embedding_model.encode(content)
        self.vector_db.add(content, embedding)
    
    def retrieve(self, query: str, limit=5):
        query_embedding = self.embedding_model.encode(query)
        return self.vector_db.search(query_embedding, limit)
```

---

## Slide 16: Integración Memoria + Herramientas
**Título:** Agentes con Memoria y Capacidades Externas

**Agente integrado completo:**
```python
class AdvancedAgent:
    def __init__(self):
        self.memory = HierarchicalMemorySystem()
        self.mcp_client = MCPClient(server_url, api_key)
        self.tools = self.setup_tools()
    
    def process_request(self, user_input: str):
        # 1. Consultar memoria relevante
        relevant_memories = self.memory.retrieve(user_input)
        context = self.build_context(relevant_memories)
        
        # 2. Determinar si necesita herramientas externas
        if self.needs_external_data(user_input):
            external_data = self.get_external_data(user_input)
            context.update(external_data)
        
        # 3. Generar respuesta
        response = self.generate_response(user_input, context)
        
        # 4. Almacenar interacción en memoria
        self.memory.store(f"User: {user_input}")
        self.memory.store(f"Agent: {response}")
        
        return response
    
    def get_external_data(self, query: str):
        """Usar herramientas MCP según la necesidad"""
        if "weather" in query.lower():
            return self.mcp_client.use_tool("weather", city=self.extract_city(query))
        elif "calculate" in query.lower():
            return self.mcp_client.use_tool("calculator", expression=self.extract_math(query))
        # ... más herramientas
```

**Ventajas de la integración:**
- Contexto rico para respuestas
- Capacidades expandidas
- Aprendizaje continuo
- Personalización basada en historial

---

## Slide 17: Desafíos y Consideraciones
**Título:** Retos en Sistemas de Memoria y Herramientas

**Desafíos técnicos:**

**1. Escalabilidad:**
- Millones de memorias → búsqueda lenta
- **Solución:** Indexing, caching, database optimization

**2. Consistencia:**
- Información contradictoria en memoria
- **Solución:** Validation rules, conflict resolution

**3. Privacidad y Seguridad:**
- Datos sensibles en memoria persistente
- **Solución:** Encryption, access controls, data retention policies

**4. Context Window Limits:**
- Demasiada información para incluir en prompt
- **Solución:** Summarization, relevance scoring, hierarchical context

**Desafíos de herramientas:**

**1. Rate Limiting:**
- APIs externas con límites de uso
- **Solución:** Intelligent caching, request batching

**2. Error Handling:**
- APIs no disponibles o con errores
- **Solución:** Graceful degradation, retry policies

**3. Security:**
- Acceso no autorizado a recursos
- **Solución:** Authentication, authorization, sandboxing

---

## Slide 18: Casos de Uso Empresariales
**Título:** Aplicaciones Prácticas de Memoria y Herramientas

**1. Asistente de Customer Support:**
```python
class SupportAgent:
    def handle_ticket(self, ticket):
        # Recuperar historial del cliente
        customer_history = self.memory.retrieve_by_customer(ticket.customer_id)
        
        # Buscar en knowledge base
        kb_results = self.mcp_client.search_kb(ticket.subject)
        
        # Consultar sistema de tickets
        similar_tickets = self.mcp_client.find_similar_tickets(ticket)
        
        # Generar respuesta personalizada
        return self.generate_solution(ticket, customer_history, kb_results)
```

**2. Analista Financiero:**
```python
class FinancialAnalyst:
    def analyze_portfolio(self, portfolio_id):
        # Recordar análisis previos
        previous_analysis = self.memory.retrieve_analysis(portfolio_id)
        
        # Obtener datos de mercado actuales
        market_data = self.mcp_client.get_market_data()
        
        # Calcular métricas
        metrics = self.mcp_client.calculate_risk_metrics(portfolio_id)
        
        # Generar reporte comparativo
        return self.generate_comparative_report(previous_analysis, market_data, metrics)
```

**3. Asistente de Investigación:**
```python
class ResearchAssistant:
    def research_topic(self, topic):
        # Consultar investigaciones previas
        past_research = self.memory.retrieve_research(topic)
        
        # Búsqueda en bases de datos académicas
        papers = self.mcp_client.search_papers(topic)
        
        # Análisis de tendencias
        trends = self.mcp_client.analyze_trends(topic)
        
        # Síntesis y nuevos insights
        return self.synthesize_findings(past_research, papers, trends)
```

---

## Slide 19: Mejores Prácticas
**Título:** Recomendaciones para Implementación

**Diseño de Memoria:**
1. **Estructura clara:** Definir tipos de memoria y sus propósitos
2. **Metadata rica:** Incluir contexto, importancia, timestamps
3. **Límites apropiados:** Evitar memory overflow con pruning strategies
4. **Indexing eficiente:** Usar estructuras de datos optimizadas para búsqueda

**Gestión de Herramientas:**
1. **Error handling robusto:** Graceful fallbacks cuando herramientas fallan
2. **Caching inteligente:** Evitar llamadas innecesarias a APIs costosas
3. **Security first:** Validation, authentication, least privilege
4. **Observability:** Logging detallado para debugging y monitoring

**Integración MCP:**
1. **Connection pooling:** Reutilizar conexiones para eficiencia
2. **Retry policies:** Manejo inteligente de fallos temporales  
3. **Resource management:** Cleanup apropiado de recursos
4. **Version compatibility:** Manejar cambios en protocolos MCP

**Performance:**
1. **Async operations:** No bloquear en operaciones I/O
2. **Batch requests:** Agrupar operaciones similares
3. **Memory optimization:** Garbage collection de memorias obsoletas
4. **Profiling:** Medir y optimizar operaciones costosas

---

## Slide 20: Próximos Pasos en RA2
**Título:** Roadmap hacia IL2.3 y IL2.4

**IL2.3 - Planning y Orchestration:**
- Algoritmos de planificación multi-paso
- Orchestration de workflows complejos
- Dynamic replanning basado en resultados
- Multi-agent coordination patterns
- **Conexión con IL2.2:** Usar memoria para informar decisiones de planning

**IL2.4 - Technical Documentation:**
- Documentación de arquitecturas de sistemas de agentes
- Design patterns para memoria y herramientas
- Deployment y operations guidelines
- Monitoring y observability frameworks
- **Conexión con IL2.2:** Documentar sistemas de memoria y integraciones MCP

**Proyecto integrador RA2:**
- Sistema completo: Memoria + Herramientas + Planning + Documentation
- Implementación de agente empresarial end-to-end
- Evaluación de performance y escalabilidad
- Deployment en entorno productivo simulado

**Preparación requerida:**
- Dominio de patrones de memoria
- Experiencia con integraciones MCP
- Comprensión de trade-offs de arquitectura
- Base sólida para sistemas complejos

---

## Slide 21: Resumen Ejecutivo
**Título:** Conceptos Clave del Módulo IL2.2

**Fundamentos adquiridos:**
1. **Sistemas de memoria** para agentes LLM (conversacional, episódica, semántica)
2. **Persistencia de memoria** entre sesiones con diferentes backends
3. **Integración de herramientas externas** para expandir capacidades
4. **Protocolo MCP** para conexiones seguras y estandarizadas
5. **Patrones avanzados** de memoria jerárquica y asociativa

**Implementaciones prácticas:**
- Sistema de memoria simple y avanzado con MemoryItem
- Herramientas externas básicas y complejas
- Cliente y servidor MCP para recursos seguros
- Agentes integrados con memoria + herramientas
- Persistencia en archivos, SQLite y vector databases

**Diferenciadores clave:**
- **Memoria vs. Stateless:** Continuidad y personalización
- **MCP vs. Direct Integration:** Seguridad y estandarización
- **Simple vs. Hierarchical Memory:** Escalabilidad y eficiencia
- **Local vs. External Tools:** Capacidades expandidas

**Preparación para IL2.3:**
- Foundation sólida en gestión de estado
- Experiencia con herramientas externas
- Comprensión de trade-offs de memoria
- Base para sistemas de planning complejos

**Impacto organizacional:**
- Agentes que aprenden y se adaptan
- Integración segura con sistemas empresariales
- Automatización de procesos que requieren contexto
- Foundation para sistemas de IA organizacional