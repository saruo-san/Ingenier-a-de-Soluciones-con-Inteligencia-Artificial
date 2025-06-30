# Presentación IL2.1 - Arquitectura y Frameworks de Agentes

## Slide 1: Título y Objetivos
**Título:** IL2.1 - Arquitectura y Frameworks de Agentes  
**Subtítulo:** Desarrollo de Agentes Inteligentes con LangChain y CrewAI

**Objetivos:**
- Comprender los fundamentos de agentes inteligentes basados en LLM
- Analizar diferentes arquitecturas y patrones de agentes
- Implementar agentes usando LangChain y CrewAI
- Dominar conceptos de function calling y herramientas
- Diseñar flujos de trabajo automatizados con equipos de agentes

---

## Slide 2: ¿Qué es un Agente Inteligente?
**Título:** Fundamentos de Agentes LLM

**Definición:**
Un agente inteligente es un sistema autónomo que puede:
- **Percibir** su entorno y datos de entrada
- **Razonar** sobre la información percibida
- **Decidir** qué acciones tomar
- **Actuar** en base a sus decisiones
- **Aprender** de los resultados para mejorar

**Ciclo básico de un agente:**
```
Percepción → Razonamiento → Decisión → Acción → Evaluación
```

**Componentes principales:**
- **LLM:** Motor de razonamiento y decisión
- **Memoria:** Contexto y historial de interacciones
- **Herramientas:** Capacidades para actuar en el mundo
- **Planificación:** Capacidad de crear y ejecutar planes

**Diferencia clave vs. LLM tradicional:**
- LLM: Entrada → Salida (una sola interacción)
- Agente: Ciclo continuo de percepción-acción con herramientas

---

## Slide 3: Tipos de Agentes LLM
**Título:** Clasificación de Agentes según Capacidades

**1. Agente Reactivo (Reactive Agent):**
- Responde inmediatamente a estímulos
- No mantiene estado complejo
- Ideal para tareas simples y directas

**2. Agente de Planificación (Planning Agent):**
- Crea planes multi-paso para objetivos complejos
- Mantiene estado y contexto entre pasos
- Puede replanificar según resultados

**3. Agente Reflexivo (Reflective Agent):**
- Evalúa sus propias acciones y resultados
- Aprende de errores y mejora estrategias
- Self-correction y meta-razonamiento

**Ejemplo de implementación:**
```python
class SimpleAgent:
    def perceive(self, input_text) -> Dict:
        return {'input': input_text, 'context': self.get_context()}
    
    def think(self, perception) -> Dict:
        decision = self.llm.predict(f"Qué hacer con: {perception}")
        return self.parse_decision(decision)
    
    def act(self, decision) -> str:
        return self.execute_action(decision['action'])
```

---

## Slide 4: Arquitecturas de Agentes
**Título:** Script 2 - Patrones Arquitectónicos

**1. Arquitectura Monolítica:**
- Todo el procesamiento en un solo componente
- Simple pero difícil de mantener y escalar

**2. Arquitectura Modular:**
- Componentes separados para diferentes funciones
- Pipeline de módulos especializados

**3. Arquitectura Basada en Eventos:**
- Comunicación mediante eventos entre componentes
- Flexible y escalable

**4. Arquitectura en Capas:**
- Diferentes niveles de abstracción
- Presentación → Negocio → Datos

**5. Arquitectura de Microservicios:**
- Servicios independientes y especializados
- Máxima flexibilidad y escalabilidad

**Comparación de características:**
- **Complejidad:** Monolítica < Modular < Capas < Eventos < Microservicios
- **Escalabilidad:** Monolítica < Modular < Capas < Eventos < Microservicios
- **Mantenimiento:** Depende del caso de uso específico

---

## Slide 5: LangChain para Agentes
**Título:** Script 4 - Framework LangChain

**¿Qué es LangChain?**
Framework para desarrollar aplicaciones con LLMs que proporciona:
- Abstracciones de alto nivel para agentes
- Integración con múltiples LLMs y herramientas
- Patrones predefinidos para casos comunes
- Sistema de memoria y contexto

**Tipos de agentes LangChain:**
1. **Zero-shot Agent:** Sin ejemplos previos, máxima flexibilidad
2. **Conversational Agent:** Optimizado para conversaciones largas
3. **Structured Chat Agent:** Salida estructurada y predecible

**Implementación básica:**
```python
from langchain.agents import initialize_agent, AgentType, Tool

# Configurar herramientas
tools = [
    Tool(name="search", func=search_web, description="Buscar en internet"),
    Tool(name="calculator", func=calculate, description="Realizar cálculos")
]

# Crear agente
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Ejecutar
result = agent.run("¿Cuál es la población de Madrid?")
```

---

## Slide 6: Herramientas y Function Calling
**Título:** Capacidades de Acción de los Agentes

**¿Qué son las herramientas?**
Funciones que permiten al agente interactuar con el mundo exterior:
- Búsqueda web
- Cálculos matemáticos
- APIs externas
- Bases de datos
- Sistemas de archivos

**Function Calling:**
Capacidad del LLM de invocar funciones estructuradas basándose en su descripción.

**Ejemplo de herramienta personalizada:**
```python
def get_weather(city: str) -> str:
    """Obtener información del clima para una ciudad"""
    # Lógica para consultar API del clima
    return f"Clima en {city}: Soleado, 25°C"

weather_tool = Tool(
    name="get_weather",
    func=get_weather,
    description="Útil para obtener información del clima actual"
)
```

**Mejores prácticas:**
- Descripciones claras y específicas
- Manejo robusto de errores
- Validación de parámetros
- Logging para debugging

---

## Slide 7: CrewAI - Equipos de Agentes
**Título:** Script 5 - Framework CrewAI

**¿Qué es CrewAI?**
Framework especializado en crear **equipos de agentes** que colaboran para completar tareas complejas.

**Conceptos clave:**
- **Agent:** Agente individual con rol específico
- **Task:** Tarea asignada a un agente
- **Crew:** Equipo de agentes trabajando juntos
- **Process:** Cómo se coordinan las tareas (secuencial, jerárquico)

**Ejemplo de equipo de investigación:**
```python
# Crear agentes especializados
researcher = Agent(
    role="Investigador",
    goal="Recopilar información exhaustiva",
    backstory="Experto en investigación con acceso a múltiples fuentes"
)

writer = Agent(
    role="Escritor",
    goal="Crear contenido claro y estructurado",
    backstory="Escritor profesional especializado en contenido técnico"
)

# Crear tareas
research_task = Task(
    description="Investigar sobre inteligencia artificial",
    agent=researcher
)

writing_task = Task(
    description="Escribir artículo basado en la investigación",
    agent=writer,
    context=[research_task]
)

# Crear equipo
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential
)
```

---

## Slide 8: Roles y Especialización en CrewAI
**Título:** Agentes Especializados en Equipos

**Roles comunes de agentes:**

**1. Investigador (Researcher):**
- **Función:** Recopilar información de múltiples fuentes
- **Herramientas:** Búsqueda web, Wikipedia, APIs
- **Salida:** Datos estructurados y verificados

**2. Escritor (Writer):**
- **Función:** Crear contenido claro y bien estructurado
- **Herramientas:** Procesamiento de texto, templates
- **Salida:** Artículos, reportes, documentación

**3. Analista (Analyst):**
- **Función:** Analizar datos y extraer insights
- **Herramientas:** Análisis estadístico, visualización
- **Salida:** Análisis, recomendaciones, insights

**4. Revisor (Reviewer):**
- **Función:** Revisar y mejorar calidad del trabajo
- **Herramientas:** Verificación, corrección
- **Salida:** Contenido mejorado y validado

**Ventajas de especialización:**
- Mayor experticia en tareas específicas
- Mejor calidad de resultados
- Posibilidad de paralelización
- Reutilización de agentes en diferentes equipos

---

## Slide 9: Procesos de Coordinación
**Título:** Cómo Colaboran los Agentes

**1. Proceso Secuencial:**
```
Agente A → Agente B → Agente C → Resultado Final
```
- Tareas se ejecutan en orden específico
- Cada agente usa la salida del anterior
- Control total sobre el flujo

**2. Proceso Jerárquico:**
```
     Manager Agent
    /      |      \
Agent A  Agent B  Agent C
```
- Un agente manager coordina a los demás
- Delegación de tareas y supervisión
- Escalabilidad para equipos grandes

**3. Proceso Concurrente:**
```
Agent A ──┐
Agent B ──┼── Agregación → Resultado
Agent C ──┘
```
- Múltiples agentes trabajan en paralelo
- Mayor velocidad de ejecución
- Requiere mecanismo de agregación

**Consideraciones:**
- Dependencias entre tareas
- Recursos compartidos
- Manejo de conflictos
- Sincronización de resultados

---

## Slide 10: Comparación LangChain vs CrewAI
**Título:** Frameworks: Cuándo Usar Cada Uno

**LangChain:**
**Fortalezas:**
- Ecosistema maduro y extenso
- Gran variedad de integraciones
- Flexibilidad en arquitecturas
- Documentación completa

**Ideal para:**
- Agentes individuales complejos
- Integración con múltiples LLMs
- Experimentación y prototipado
- Casos de uso diversos

**CrewAI:**
**Fortalezas:**
- Especializado en equipos de agentes
- Coordinación automática entre agentes
- Roles y responsabilidades claras
- Procesos de workflow definidos

**Ideal para:**
- Tareas complejas multi-paso
- Especialización de agentes
- Flujos de trabajo estructurados
- Proyectos que requieren colaboración

**Criterios de selección:**
- **Complejidad de la tarea:** Simple → LangChain, Compleja → CrewAI
- **Número de agentes:** Uno → LangChain, Múltiples → CrewAI
- **Especialización:** General → LangChain, Específica → CrewAI

---

## Slide 11: Memoria y Estado en Agentes
**Título:** Gestión de Contexto e Información

**Tipos de memoria:**

**1. Memoria de Trabajo (Working Memory):**
- Información temporal para la tarea actual
- Se limpia entre sesiones
- Equivale al "scratchpad" del agente

**2. Memoria Episódica:**
- Historial de interacciones y experiencias
- Permite aprender de errores pasados
- Base para mejora continua

**3. Memoria Semántica:**
- Conocimiento general y hechos
- Información del dominio específico
- Actualizable con nueva información

**Implementación en LangChain:**
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    memory=memory,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION
)
```

**Consideraciones:**
- Límites de contexto del LLM
- Persistencia entre sesiones
- Privacidad y seguridad de datos

---

## Slide 12: Planificación y Estrategias
**Título:** Agentes que Planifican y Ejecutan

**Tipos de planificación:**

**1. Planificación Reactiva:**
- Decide acción siguiente basada en estado actual
- No anticipa pasos futuros
- Rápida pero puede ser ineficiente

**2. Planificación Anticipada:**
- Crea plan completo antes de ejecutar
- Considera múltiples pasos y dependencias
- Más eficiente pero requiere más procesamiento

**3. Planificación Híbrida:**
- Plan inicial con re-planificación según resultados
- Balance entre eficiencia y adaptabilidad
- Maneja incertidumbre mejor

**Ejemplo de agente planificador:**
```python
class PlanningAgent:
    def create_plan(self, goal: str) -> List[str]:
        prompt = f"""Objetivo: {goal}
        Herramientas disponibles: {self.tools}
        
        Crea plan paso a paso:
        1. [primer paso]
        2. [segundo paso]
        ..."""
        
        plan = self.llm.predict(prompt)
        return self.parse_plan(plan)
    
    def execute_plan(self, goal: str):
        plan = self.create_plan(goal)
        for step in plan:
            result = self.execute_step(step)
            if not self.validate_result(result):
                plan = self.replan(goal, step, result)
```

---

## Slide 13: Herramientas Avanzadas e Integraciones
**Título:** Expandiendo Capacidades de Agentes

**Categorías de herramientas:**

**1. Búsqueda y Recuperación:**
- Búsqueda web (DuckDuckGo, Google)
- Bases de datos vectoriales
- Wikipedia, APIs de conocimiento

**2. Cálculo y Análisis:**
- Calculadora matemática
- Análisis estadístico
- Procesamiento de datos

**3. Comunicación:**
- Email, Slack, APIs de chat
- Generación de reportes
- Notificaciones

**4. Sistemas Externos:**
- APIs REST
- Bases de datos SQL/NoSQL
- Sistemas de archivos

**Ejemplo de integración con API:**
```python
def get_stock_price(symbol: str) -> str:
    """Obtener precio actual de una acción"""
    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    
    response = requests.get(url)
    data = response.json()
    
    if "Global Quote" in data:
        price = data["Global Quote"]["05. price"]
        return f"Precio actual de {symbol}: ${price}"
    else:
        return f"No se pudo obtener precio para {symbol}"

stock_tool = Tool(
    name="stock_price",
    func=get_stock_price,
    description="Obtiene el precio actual de una acción"
)
```

---

## Slide 14: Evaluación de Agentes
**Título:** Métricas y Evaluación de Performance

**Métricas de evaluación:**

**1. Efectividad:**
- **Task Success Rate:** Porcentaje de tareas completadas exitosamente
- **Goal Achievement:** Cumplimiento de objetivos específicos
- **Quality Score:** Calidad de las salidas generadas

**2. Eficiencia:**
- **Time to Completion:** Tiempo para completar tareas
- **Resource Usage:** Uso de tokens, llamadas API, memoria
- **Cost per Task:** Costo asociado por tarea completada

**3. Confiabilidad:**
- **Error Rate:** Frecuencia de errores o fallos
- **Consistency:** Consistencia en resultados similares
- **Recovery Time:** Tiempo para recuperarse de errores

**Framework de evaluación:**
```python
class AgentEvaluator:
    def evaluate_task_success(self, agent, test_cases):
        success_count = 0
        for test_case in test_cases:
            result = agent.run(test_case.input)
            if self.validate_output(result, test_case.expected):
                success_count += 1
        return success_count / len(test_cases)
    
    def measure_efficiency(self, agent, task):
        start_time = time.time()
        token_count_before = agent.get_token_usage()
        
        result = agent.run(task)
        
        execution_time = time.time() - start_time
        tokens_used = agent.get_token_usage() - token_count_before
        
        return {
            'execution_time': execution_time,
            'tokens_used': tokens_used,
            'cost': self.calculate_cost(tokens_used)
        }
```

---

## Slide 15: Casos de Uso Empresariales
**Título:** Aplicaciones Prácticas de Agentes

**Automatización de Procesos:**
- **Customer Support:** Agentes que resuelven tickets automáticamente
- **Data Processing:** Pipeline de análisis de datos automatizado
- **Content Creation:** Generación de contenido para marketing

**Investigación y Análisis:**
- **Market Research:** Equipos que investigan mercados y competencia
- **Scientific Research:** Revisión de literatura y síntesis
- **Financial Analysis:** Análisis de mercados y recomendaciones

**Asistentes Especializados:**
- **Legal Assistant:** Revisión de contratos y compliance
- **Medical Assistant:** Análisis de síntomas y recomendaciones
- **Engineering Assistant:** Debugging y optimización de código

**Ejemplo: Agente de Customer Support:**
```python
support_researcher = Agent(
    role="Support Researcher",
    goal="Investigar problemas técnicos en base de conocimiento",
    tools=[knowledge_base_search, ticket_history_search]
)

solution_writer = Agent(
    role="Solution Writer", 
    goal="Crear respuestas claras y útiles para clientes",
    tools=[template_generator, email_formatter]
)

quality_reviewer = Agent(
    role="Quality Reviewer",
    goal="Verificar precisión y tono de respuestas",
    tools=[sentiment_analyzer, fact_checker]
)
```

---

## Slide 16: Mejores Prácticas
**Título:** Recomendaciones para Desarrollo de Agentes

**Diseño de Agentes:**
1. **Principio de Responsabilidad Única:** Cada agente debe tener un propósito claro
2. **Composición sobre Herencia:** Usar herramientas modulares
3. **Fail Fast:** Detectar errores temprano y manejarlos apropiadamente
4. **Observabilidad:** Logging detallado para debugging

**Gestión de Herramientas:**
1. **Descripciones Claras:** Herramientas bien documentadas
2. **Validación de Entrada:** Verificar parámetros antes de ejecución
3. **Manejo de Errores:** Graceful degradation ante fallos
4. **Rate Limiting:** Respetar límites de APIs externas

**Optimización de Performance:**
1. **Caching:** Almacenar resultados de operaciones costosas
2. **Paralelización:** Ejecutar tareas independientes en paralelo
3. **Lazy Loading:** Cargar recursos solo cuando sea necesario
4. **Circuit Breakers:** Proteger contra cascading failures

**Seguridad:**
1. **Validación de Input:** Sanitizar todas las entradas
2. **Principio de Menor Privilegio:** Acceso mínimo necesario
3. **Audit Trails:** Registro de todas las acciones
4. **Secrets Management:** Manejo seguro de API keys

---

## Slide 17: Debugging y Troubleshooting
**Título:** Identificación y Resolución de Problemas

**Problemas comunes:**

**1. Loops Infinitos:**
- Agente repite la misma acción
- **Solución:** Límites de iteración, detección de patrones

**2. Hallucination en Herramientas:**
- Agente inventa herramientas o parámetros
- **Solución:** Validación estricta, manejo de errores

**3. Context Overflow:**
- Excede límites de contexto del LLM
- **Solución:** Gestión de memoria, summarización

**4. Poor Tool Selection:**
- Usa herramientas inapropiadas para la tarea
- **Solución:** Mejores descripciones, ejemplos

**Estrategias de debugging:**
```python
class DebuggableAgent:
    def __init__(self, llm, tools, debug_mode=False):
        self.debug_mode = debug_mode
        self.execution_log = []
    
    def log_step(self, step_type, data):
        if self.debug_mode:
            self.execution_log.append({
                'timestamp': time.time(),
                'type': step_type,
                'data': data
            })
    
    def run_with_debugging(self, query):
        self.log_step('input', query)
        
        try:
            result = self.run(query)
            self.log_step('success', result)
            return result
        except Exception as e:
            self.log_step('error', str(e))
            raise
    
    def print_execution_log(self):
        for entry in self.execution_log:
            print(f"[{entry['timestamp']}] {entry['type']}: {entry['data']}")
```

---

## Slide 18: Tendencias y Futuro
**Título:** Evolución de Agentes Inteligentes

**Tendencias emergentes:**

**1. Multimodal Agents:**
- Agentes que trabajan con texto, imágenes, audio
- Comprensión más rica del contexto
- Interacciones más naturales

**2. Autonomous Agents:**
- Agentes que operan independientemente por períodos largos
- Auto-mejora y adaptación
- Minimal human supervision

**3. Agent Societies:**
- Ecosistemas complejos de agentes interactuando
- Emergent behaviors y colaboración
- Economías de agentes

**4. Specialized Domains:**
- Agentes específicos para medicina, legal, finanzas
- Deep domain expertise
- Integración con herramientas profesionales

**Desafíos técnicos:**
- Escalabilidad de coordinación
- Confiabilidad y robustez
- Explicabilidad de decisiones
- Alineación con objetivos humanos

**Oportunidades:**
- Automatización de trabajo cognitivo
- Democratización de expertise
- Aceleración de investigación y desarrollo
- Nuevos modelos de negocio

---

## Slide 19: Próximos Pasos en RA2
**Título:** Roadmap del Módulo RA2

**IL2.2 - Memory Systems y Tool Integration:**
- Sistemas de memoria avanzados
- Model Context Protocol (MCP)
- Integración de herramientas externas
- Persistent agent state

**IL2.3 - Planning y Orchestration:**
- Algoritmos de planificación avanzados
- Orchestration de workflows complejos
- Multi-agent coordination patterns
- Dynamic replanning strategies

**IL2.4 - Technical Documentation:**
- Documentación de arquitecturas de agentes
- Design patterns para sistemas de agentes
- Deployment y operations
- Monitoring y observability

**Proyecto integrador:**
- Diseño de sistema de agentes completo
- Implementación end-to-end
- Evaluación y optimización
- Presentación y documentación

---

## Slide 20: Resumen Ejecutivo
**Título:** Conceptos Clave del Módulo IL2.1

**Fundamentos adquiridos:**
1. **Arquitecturas de agentes** desde monolíticas hasta microservicios
2. **Ciclo percepción-decisión-acción** como base de agentes inteligentes
3. **LangChain** para agentes individuales flexibles y potentes
4. **CrewAI** para equipos colaborativos de agentes especializados
5. **Function calling** y herramientas para capacidades de acción

**Implementaciones prácticas:**
- Agentes simples, reactivos y planificadores
- Integración con APIs y sistemas externos
- Equipos especializados (investigador, escritor, analista)
- Herramientas personalizadas y reutilizables
- Sistemas de memoria y contexto

**Diferenciadores clave:**
- **LangChain:** Flexibilidad y ecosistema maduro
- **CrewAI:** Especialización y coordinación automática
- **Arquitecturas:** Trade-offs entre simplicidad y escalabilidad
- **Herramientas:** Extensión de capacidades más allá del LLM

**Preparación para IL2.2:**
- Foundation sólida en frameworks de agentes
- Comprensión de patrones arquitectónicos
- Experiencia con herramientas y function calling
- Conocimiento de coordinación entre agentes
- Base para memory systems y MCP integration

**Impacto organizacional:**
- Automatización de procesos cognitivos complejos
- Especialización y expertise escalable
- Workflows inteligentes y adaptativos
- Foundation para transformación digital con IA