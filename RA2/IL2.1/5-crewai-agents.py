"""
IL2.1: Agentes con CrewAI
========================

Este módulo explora la implementación de agentes usando el framework CrewAI,
que permite crear equipos de agentes especializados que colaboran entre sí.
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importaciones de CrewAI
try:
    from crewai import Agent, Task, Crew, Process
    from crewai.tools import BaseTool
    from langchain.tools import DuckDuckGoSearchRun
    from langchain.utilities import WikipediaAPIWrapper
except ImportError:
    print("⚠️ CrewAI no está instalado. Instalando...")
    import subprocess
    subprocess.check_call(["pip", "install", "crewai", "duckduckgo-search", "wikipedia"])
    from crewai import Agent, Task, Crew, Process
    from crewai.tools import BaseTool
    from langchain.tools import DuckDuckGoSearchRun
    from langchain.utilities import WikipediaAPIWrapper


class CrewAIManager:
    """Gestor de agentes CrewAI"""
    
    def __init__(self):
        self.agents = {}
        self.tools = {}
        self.crews = {}
    
    def setup_tools(self):
        """Configurar herramientas básicas"""
        # Herramienta de búsqueda web
        search_tool = DuckDuckGoSearchRun()
        self.tools["search"] = search_tool
        
        # Herramienta de Wikipedia
        wiki_tool = WikipediaAPIWrapper()
        self.tools["wikipedia"] = wiki_tool
        
        print(f"✅ {len(self.tools)} herramientas configuradas")
    
    def create_researcher_agent(self, name: str = "researcher") -> Agent:
        """Crear agente investigador"""
        agent = Agent(
            role="Investigador",
            goal="Realizar investigaciones exhaustivas y encontrar información relevante",
            backstory="""Eres un investigador experto con años de experiencia en 
            recopilar y analizar información de múltiples fuentes. Tu trabajo es 
            encontrar datos precisos y relevantes para cualquier tema.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.tools["search"], self.tools["wikipedia"]]
        )
        
        self.agents[name] = agent
        print(f"✅ Agente investigador creado: {name}")
        return agent
    
    def create_writer_agent(self, name: str = "writer") -> Agent:
        """Crear agente escritor"""
        agent = Agent(
            role="Escritor",
            goal="Crear contenido claro, conciso y bien estructurado",
            backstory="""Eres un escritor profesional con experiencia en crear 
            contenido atractivo y fácil de entender. Tu trabajo es transformar 
            información compleja en textos claros y bien organizados.""",
            verbose=True,
            allow_delegation=False
        )
        
        self.agents[name] = agent
        print(f"✅ Agente escritor creado: {name}")
        return agent
    
    def create_analyst_agent(self, name: str = "analyst") -> Agent:
        """Crear agente analista"""
        agent = Agent(
            role="Analista",
            goal="Analizar datos y extraer insights valiosos",
            backstory="""Eres un analista de datos experto con habilidades en 
            interpretar información compleja y encontrar patrones. Tu trabajo es 
            proporcionar análisis profundos y recomendaciones basadas en datos.""",
            verbose=True,
            allow_delegation=False
        )
        
        self.agents[name] = agent
        print(f"✅ Agente analista creado: {name}")
        return agent
    
    def create_reviewer_agent(self, name: str = "reviewer") -> Agent:
        """Crear agente revisor"""
        agent = Agent(
            role="Revisor",
            goal="Revisar y mejorar la calidad del trabajo de otros agentes",
            backstory="""Eres un revisor experto con un ojo agudo para detectar 
            errores y oportunidades de mejora. Tu trabajo es asegurar que todo 
            el contenido sea preciso, claro y de alta calidad.""",
            verbose=True,
            allow_delegation=False
        )
        
        self.agents[name] = agent
        print(f"✅ Agente revisor creado: {name}")
        return agent
    
    def create_research_task(self, topic: str) -> Task:
        """Crear tarea de investigación"""
        task = Task(
            description=f"""Realiza una investigación exhaustiva sobre: {topic}
            
            Tu investigación debe incluir:
            1. Información básica y definiciones
            2. Historia y evolución del tema
            3. Aplicaciones actuales
            4. Tendencias y desarrollos futuros
            
            Proporciona información detallada y bien estructurada.""",
            agent=self.agents["researcher"],
            expected_output="Reporte de investigación detallado con información estructurada"
        )
        return task
    
    def create_writing_task(self, research_data: str) -> Task:
        """Crear tarea de escritura"""
        task = Task(
            description=f"""Basándote en la investigación proporcionada, crea un 
            artículo bien estructurado y fácil de entender.
            
            Datos de investigación: {research_data}
            
            El artículo debe incluir:
            1. Introducción clara
            2. Desarrollo del tema
            3. Conclusiones
            4. Referencias si es necesario
            
            Asegúrate de que el contenido sea accesible para una audiencia general.""",
            agent=self.agents["writer"],
            expected_output="Artículo completo y bien estructurado"
        )
        return task
    
    def create_analysis_task(self, content: str) -> Task:
        """Crear tarea de análisis"""
        task = Task(
            description=f"""Analiza el contenido proporcionado y extrae insights 
            valiosos y recomendaciones.
            
            Contenido a analizar: {content}
            
            Tu análisis debe incluir:
            1. Puntos clave identificados
            2. Fortalezas y debilidades
            3. Oportunidades de mejora
            4. Recomendaciones específicas
            
            Proporciona un análisis profundo y útil.""",
            agent=self.agents["analyst"],
            expected_output="Análisis detallado con insights y recomendaciones"
        )
        return task
    
    def create_review_task(self, content: str) -> Task:
        """Crear tarea de revisión"""
        task = Task(
            description=f"""Revisa el contenido proporcionado y sugiere mejoras 
            para la calidad, claridad y precisión.
            
            Contenido a revisar: {content}
            
            Tu revisión debe incluir:
            1. Corrección de errores gramaticales y ortográficos
            2. Mejoras en la claridad y estructura
            3. Verificación de precisión factual
            4. Sugerencias de mejora general
            
            Proporciona una revisión constructiva y detallada.""",
            agent=self.agents["reviewer"],
            expected_output="Revisión completa con correcciones y sugerencias"
        )
        return task
    
    def create_research_crew(self, name: str = "research_crew") -> Crew:
        """Crear equipo de investigación"""
        # Crear agentes si no existen
        if "researcher" not in self.agents:
            self.create_researcher_agent()
        if "writer" not in self.agents:
            self.create_writer_agent()
        if "reviewer" not in self.agents:
            self.create_reviewer_agent()
        
        # Crear tareas
        research_task = self.create_research_task("inteligencia artificial")
        writing_task = self.create_writing_task("{{research_data}}")
        review_task = self.create_review_task("{{final_article}}")
        
        # Configurar dependencias
        writing_task.context = [research_task]
        review_task.context = [writing_task]
        
        # Crear equipo
        crew = Crew(
            agents=[self.agents["researcher"], self.agents["writer"], self.agents["reviewer"]],
            tasks=[research_task, writing_task, review_task],
            verbose=True,
            process=Process.sequential
        )
        
        self.crews[name] = crew
        print(f"✅ Equipo de investigación creado: {name}")
        return crew
    
    def create_analysis_crew(self, name: str = "analysis_crew") -> Crew:
        """Crear equipo de análisis"""
        # Crear agentes si no existen
        if "researcher" not in self.agents:
            self.create_researcher_agent()
        if "analyst" not in self.agents:
            self.create_analyst_agent()
        if "writer" not in self.agents:
            self.create_writer_agent()
        
        # Crear tareas
        research_task = self.create_research_task("machine learning")
        analysis_task = self.create_analysis_task("{{research_data}}")
        writing_task = self.create_writing_task("{{analysis_results}}")
        
        # Configurar dependencias
        analysis_task.context = [research_task]
        writing_task.context = [analysis_task]
        
        # Crear equipo
        crew = Crew(
            agents=[self.agents["researcher"], self.agents["analyst"], self.agents["writer"]],
            tasks=[research_task, analysis_task, writing_task],
            verbose=True,
            process=Process.sequential
        )
        
        self.crews[name] = crew
        print(f"✅ Equipo de análisis creado: {name}")
        return crew
    
    def run_crew(self, crew_name: str) -> str:
        """Ejecutar equipo"""
        if crew_name not in self.crews:
            print(f"❌ Equipo '{crew_name}' no encontrado")
            return None
        
        try:
            crew = self.crews[crew_name]
            result = crew.kickoff()
            return result
        except Exception as e:
            print(f"❌ Error ejecutando equipo: {e}")
            return f"Error: {e}"


class CustomCrewAITool(BaseTool):
    """Herramienta personalizada para CrewAI"""
    
    name: str = "custom_tool"
    description: str = "Una herramienta personalizada"
    
    def _run(self, input_text: str) -> str:
        """Ejecutar la herramienta"""
        return f"Resultado de herramienta personalizada: {input_text}"


def demo_crewai_agents():
    """Demostración de agentes CrewAI"""
    print("🤖 DEMOSTRACIÓN: Agentes CrewAI")
    print("=" * 50)
    
    # Crear gestor
    manager = CrewAIManager()
    manager.setup_tools()
    
    # Crear agentes individuales
    print("\n1️⃣ Creando agentes individuales...")
    researcher = manager.create_researcher_agent()
    writer = manager.create_writer_agent()
    analyst = manager.create_analyst_agent()
    reviewer = manager.create_reviewer_agent()
    
    print(f"✅ {len(manager.agents)} agentes creados")
    
    # Crear equipos
    print("\n2️⃣ Creando equipos...")
    research_crew = manager.create_research_crew()
    analysis_crew = manager.create_analysis_crew()
    
    print(f"✅ {len(manager.crews)} equipos creados")


def demo_crew_execution():
    """Demostración de ejecución de equipos"""
    print("\n🚀 DEMOSTRACIÓN: Ejecución de Equipos")
    print("=" * 50)
    
    # Nota: En una implementación real, esto ejecutaría los equipos
    # Aquí mostramos la estructura sin ejecutar para evitar costos de API
    
    print("📋 Estructura de equipos CrewAI:")
    print("\n🔬 Equipo de Investigación:")
    print("  1. Investigador → Recopila información")
    print("  2. Escritor → Crea artículo")
    print("  3. Revisor → Mejora calidad")
    
    print("\n📊 Equipo de Análisis:")
    print("  1. Investigador → Recopila datos")
    print("  2. Analista → Extrae insights")
    print("  3. Escritor → Crea reporte")
    
    print("\n💡 Para ejecutar equipos reales:")
    print("  - Configurar API keys")
    print("  - Usar manager.run_crew('research_crew')")
    print("  - Los agentes colaborarán automáticamente")


def demo_agent_roles():
    """Demostración de roles de agentes"""
    print("\n👥 DEMOSTRACIÓN: Roles de Agentes")
    print("=" * 50)
    
    roles = {
        "Investigador": {
            "Función": "Recopilar información de múltiples fuentes",
            "Herramientas": "Búsqueda web, Wikipedia",
            "Salida": "Datos estructurados y verificados"
        },
        "Escritor": {
            "Función": "Crear contenido claro y bien estructurado",
            "Herramientas": "Procesamiento de texto",
            "Salida": "Artículos, reportes, documentación"
        },
        "Analista": {
            "Función": "Analizar datos y extraer insights",
            "Herramientas": "Análisis estadístico, interpretación",
            "Salida": "Análisis, recomendaciones, insights"
        },
        "Revisor": {
            "Función": "Revisar y mejorar la calidad del trabajo",
            "Herramientas": "Verificación, corrección",
            "Salida": "Contenido mejorado y validado"
        }
    }
    
    for role, info in roles.items():
        print(f"\n👤 {role}:")
        for key, value in info.items():
            print(f"  {key}: {value}")


def demo_crew_processes():
    """Demostración de procesos de equipos"""
    print("\n🔄 DEMOSTRACIÓN: Procesos de Equipos")
    print("=" * 50)
    
    processes = {
        "Sequential": {
            "Descripción": "Tareas se ejecutan en secuencia",
            "Ventajas": "Control total, dependencias claras",
            "Desventajas": "Más lento, sin paralelización",
            "Casos de uso": "Flujos de trabajo lineales"
        },
        "Hierarchical": {
            "Descripción": "Tareas se organizan en jerarquías",
            "Ventajas": "Estructura clara, delegación",
            "Desventajas": "Complejidad de gestión",
            "Casos de uso": "Proyectos complejos"
        }
    }
    
    for process, info in processes.items():
        print(f"\n🔄 {process}:")
        for key, value in info.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    demo_crewai_agents()
    demo_crew_execution()
    demo_agent_roles()
    demo_crew_processes() 