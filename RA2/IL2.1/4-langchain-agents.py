"""
IL2.1: Agentes con LangChain
===========================

Este módulo explora la implementación de agentes usando el framework LangChain,
incluyendo diferentes tipos de agentes, herramientas y configuración.
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importaciones de LangChain
try:
    from langchain.agents import initialize_agent, AgentType, Tool
    from langchain.llms import OpenAI
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    from langchain.memory import ConversationBufferMemory
    from langchain.prompts import MessagesPlaceholder
    from langchain.tools import DuckDuckGoSearchRun
    from langchain.utilities import WikipediaAPIWrapper
    from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
    from langchain.tools.playwright.utils import create_sync_playwright_browser
except ImportError:
    print("⚠️ LangChain no está instalado. Instalando...")
    import subprocess
    subprocess.check_call(["pip", "install", "langchain", "openai", "duckduckgo-search", "wikipedia", "playwright"])
    from langchain.agents import initialize_agent, AgentType, Tool
    from langchain.llms import OpenAI
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    from langchain.memory import ConversationBufferMemory
    from langchain.prompts import MessagesPlaceholder
    from langchain.tools import DuckDuckGoSearchRun
    from langchain.utilities import WikipediaAPIWrapper


class LangChainAgentManager:
    """Gestor de agentes LangChain"""
    
    def __init__(self):
        self.llm = None
        self.tools = []
        self.memory = None
        self.agents = {}
    
    def setup_llm(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0):
        """Configurar modelo de lenguaje"""
        try:
            if model_name.startswith("gpt"):
                self.llm = ChatOpenAI(
                    model_name=model_name,
                    temperature=temperature,
                    openai_api_key=os.getenv("OPENAI_API_KEY")
                )
            else:
                self.llm = OpenAI(
                    model_name=model_name,
                    temperature=temperature,
                    openai_api_key=os.getenv("OPENAI_API_KEY")
                )
            print(f"✅ LLM configurado: {model_name}")
        except Exception as e:
            print(f"❌ Error configurando LLM: {e}")
            # Usar LLM simulado para demostración
            self.llm = MockLLM()
    
    def setup_basic_tools(self):
        """Configurar herramientas básicas"""
        # Herramienta de búsqueda web
        search = DuckDuckGoSearchRun()
        search_tool = Tool(
            name="web_search",
            func=search.run,
            description="Útil para buscar información actual en internet"
        )
        
        # Herramienta de Wikipedia
        wikipedia = WikipediaAPIWrapper()
        wiki_tool = Tool(
            name="wikipedia",
            func=wikipedia.run,
            description="Útil para buscar información en Wikipedia"
        )
        
        # Herramienta de cálculo
        calc_tool = Tool(
            name="calculator",
            func=self.calculate,
            description="Útil para realizar cálculos matemáticos"
        )
        
        self.tools = [search_tool, wiki_tool, calc_tool]
        print(f"✅ {len(self.tools)} herramientas configuradas")
    
    def calculate(self, expression: str) -> str:
        """Herramienta de cálculo"""
        try:
            # Evaluar expresión matemática de forma segura
            allowed_names = {
                k: v for k, v in __builtins__.items() 
                if k in ['abs', 'round', 'min', 'max', 'sum']
            }
            allowed_names.update({
                'pi': 3.14159265359,
                'e': 2.71828182846
            })
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return str(result)
        except Exception as e:
            return f"Error en el cálculo: {e}"
    
    def setup_memory(self, memory_type: str = "conversation"):
        """Configurar sistema de memoria"""
        if memory_type == "conversation":
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        print(f"✅ Memoria configurada: {memory_type}")
    
    def create_zero_shot_agent(self, name: str = "zero_shot_agent"):
        """Crear agente zero-shot (sin ejemplos previos)"""
        if not self.llm or not self.tools:
            print("❌ LLM y herramientas deben estar configurados")
            return None
        
        agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            handle_parsing_errors=True
        )
        
        self.agents[name] = agent
        print(f"✅ Agente zero-shot creado: {name}")
        return agent
    
    def create_conversational_agent(self, name: str = "conversational_agent"):
        """Crear agente conversacional"""
        if not self.llm or not self.tools:
            print("❌ LLM y herramientas deben estar configurados")
            return None
        
        agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            handle_parsing_errors=True
        )
        
        self.agents[name] = agent
        print(f"✅ Agente conversacional creado: {name}")
        return agent
    
    def create_structured_chat_agent(self, name: str = "structured_chat_agent"):
        """Crear agente de chat estructurado"""
        if not self.llm or not self.tools:
            print("❌ LLM y herramientas deben estar configurados")
            return None
        
        agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            handle_parsing_errors=True
        )
        
        self.agents[name] = agent
        print(f"✅ Agente de chat estructurado creado: {name}")
        return agent
    
    def run_agent(self, agent_name: str, query: str) -> str:
        """Ejecutar agente con una consulta"""
        if agent_name not in self.agents:
            print(f"❌ Agente '{agent_name}' no encontrado")
            return None
        
        try:
            agent = self.agents[agent_name]
            result = agent.run(query)
            return result
        except Exception as e:
            print(f"❌ Error ejecutando agente: {e}")
            return f"Error: {e}"


class CustomTool:
    """Herramienta personalizada para LangChain"""
    
    def __init__(self, name: str, func, description: str):
        self.name = name
        self.func = func
        self.description = description
    
    def run(self, input_text: str) -> str:
        """Ejecutar la herramienta"""
        return self.func(input_text)


def create_custom_tools() -> List[Tool]:
    """Crear herramientas personalizadas"""
    
    def get_current_time(input_text: str) -> str:
        """Obtener hora actual"""
        from datetime import datetime
        return f"Hora actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    def get_weather(input_text: str) -> str:
        """Obtener información del clima (simulado)"""
        return f"Clima simulado para {input_text}: Soleado, 25°C"
    
    def translate_text(input_text: str) -> str:
        """Traducir texto (simulado)"""
        return f"Traducción simulada: {input_text} -> [traducción]"
    
    tools = [
        Tool(
            name="current_time",
            func=get_current_time,
            description="Obtener la hora y fecha actual"
        ),
        Tool(
            name="weather",
            func=get_weather,
            description="Obtener información del clima para una ciudad"
        ),
        Tool(
            name="translator",
            func=translate_text,
            description="Traducir texto a diferentes idiomas"
        )
    ]
    
    return tools


class MockLLM:
    """LLM simulado para demostración"""
    
    def __call__(self, prompt: str) -> str:
        if "buscar" in prompt.lower():
            return "Buscando información en internet..."
        elif "calcular" in prompt.lower():
            return "Realizando cálculo matemático..."
        elif "wikipedia" in prompt.lower():
            return "Buscando en Wikipedia..."
        else:
            return "Procesando consulta..."


def demo_langchain_agents():
    """Demostración de agentes LangChain"""
    print("🤖 DEMOSTRACIÓN: Agentes LangChain")
    print("=" * 50)
    
    # Crear gestor de agentes
    manager = LangChainAgentManager()
    
    # Configurar componentes
    manager.setup_llm()
    manager.setup_basic_tools()
    manager.setup_memory()
    
    # Crear diferentes tipos de agentes
    print("\n1️⃣ Creando agentes...")
    zero_shot = manager.create_zero_shot_agent("zero_shot")
    conversational = manager.create_conversational_agent("conversational")
    structured = manager.create_structured_chat_agent("structured")
    
    # Probar agentes
    queries = [
        "¿Cuál es la capital de Francia?",
        "Calcula 15 * 23",
        "¿Qué es la inteligencia artificial?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n📝 Consulta {i}: {query}")
        
        print("  🤖 Zero-shot agent:")
        result = manager.run_agent("zero_shot", query)
        print(f"    Resultado: {result}")
        
        print("  💬 Conversational agent:")
        result = manager.run_agent("conversational", query)
        print(f"    Resultado: {result}")


def demo_custom_tools():
    """Demostración de herramientas personalizadas"""
    print("\n🛠️ DEMOSTRACIÓN: Herramientas Personalizadas")
    print("=" * 50)
    
    tools = create_custom_tools()
    
    for tool in tools:
        print(f"\n🔧 Herramienta: {tool.name}")
        print(f"   Descripción: {tool.description}")
        result = tool.run("prueba")
        print(f"   Resultado: {result}")


def demo_agent_comparison():
    """Comparar diferentes tipos de agentes"""
    print("\n📊 COMPARACIÓN DE AGENTES LANGCHAIN")
    print("=" * 50)
    
    comparison = {
        "Zero-shot": {
            "Descripción": "Agente que no requiere ejemplos previos",
            "Ventajas": "Flexible, no necesita entrenamiento",
            "Desventajas": "Puede ser menos preciso",
            "Casos de uso": "Tareas generales, exploración"
        },
        "Conversational": {
            "Descripción": "Agente optimizado para conversaciones",
            "Ventajas": "Mantiene contexto, respuestas naturales",
            "Desventajas": "Puede ser más lento",
            "Casos de uso": "Chatbots, asistentes conversacionales"
        },
        "Structured Chat": {
            "Descripción": "Agente con salida estructurada",
            "Ventajas": "Respuestas consistentes, fácil de procesar",
            "Desventajas": "Menos flexible",
            "Casos de uso": "APIs, integración con sistemas"
        }
    }
    
    for agent_type, info in comparison.items():
        print(f"\n🤖 {agent_type}:")
        for key, value in info.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    demo_langchain_agents()
    demo_custom_tools()
    demo_agent_comparison() 