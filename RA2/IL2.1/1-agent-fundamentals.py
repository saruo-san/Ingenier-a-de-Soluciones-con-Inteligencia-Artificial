"""
IL2.1: Fundamentos de Agentes LLM
================================

Este módulo explora los conceptos fundamentales de agentes inteligentes basados en LLM,
incluyendo componentes principales, ciclos de percepción-decisión-acción y tipos de agentes.
"""

import os
from typing import Dict, List, Any
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class SimpleAgent:
    """
    Agente simple que implementa el ciclo básico de percepción-decisión-acción
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.memory = []
        self.state = {}
    
    def perceive(self, input_text: str) -> Dict[str, Any]:
        """Procesar entrada del usuario"""
        return {
            'input': input_text,
            'timestamp': '2024-01-01 12:00:00',
            'context': self.get_context()
        }
    
    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar y decidir qué hacer"""
        prompt = f"""
        Contexto: {perception['context']}
        Entrada: {perception['input']}
        
        ¿Qué acción debería tomar? Responde con:
        - ACCION: [nombre de la acción]
        - RAZON: [explicación]
        """
        
        response = self.llm.predict(prompt)
        return self.parse_decision(response)
    
    def act(self, decision: Dict[str, Any]) -> str:
        """Ejecutar la acción decidida"""
        if decision['action'] == 'respond':
            return self.generate_response(decision['reason'])
        elif decision['action'] == 'search':
            return self.search_information(decision['reason'])
        else:
            return "No entiendo esa acción"
    
    def get_context(self) -> str:
        """Obtener contexto de la conversación"""
        return "Conversación en curso"
    
    def parse_decision(self, response: str) -> Dict[str, Any]:
        """Parsear la decisión del LLM"""
        return {
            'action': 'respond',
            'reason': response
        }
    
    def generate_response(self, reason: str) -> str:
        """Generar respuesta basada en la razón"""
        return f"Basándome en: {reason}"
    
    def search_information(self, query: str) -> str:
        """Buscar información"""
        return f"Buscando información sobre: {query}"
    
    def run(self, input_text: str) -> str:
        """Ejecutar el ciclo completo"""
        # 1. Percepción
        perception = self.perceive(input_text)
        print(f"🔍 Percepción: {perception['input']}")
        
        # 2. Decisión
        decision = self.think(perception)
        print(f"🧠 Decisión: {decision['action']} - {decision['reason']}")
        
        # 3. Acción
        result = self.act(decision)
        print(f"⚡ Acción: {result}")
        
        return result


class ReactiveAgent:
    """
    Agente reactivo que responde inmediatamente sin planificación compleja
    """
    
    def __init__(self, llm, tools: List[Any]):
        self.llm = llm
        self.tools = tools
    
    def respond(self, input_text: str) -> str:
        """Respuesta inmediata basada en herramientas disponibles"""
        tool_names = [tool.name for tool in self.tools]
        
        prompt = f"""
        Herramientas disponibles: {tool_names}
        Entrada: {input_text}
        
        ¿Qué herramienta debería usar? Responde solo con el nombre de la herramienta.
        """
        
        tool_choice = self.llm.predict(prompt).strip()
        
        # Ejecutar herramienta
        for tool in self.tools:
            if tool.name == tool_choice:
                return tool.func(input_text)
        
        return "No encontré una herramienta apropiada"


class PlanningAgent:
    """
    Agente con planificación que organiza múltiples pasos para lograr objetivos
    """
    
    def __init__(self, llm, tools: List[Any]):
        self.llm = llm
        self.tools = tools
        self.plan = []
    
    def create_plan(self, goal: str) -> List[str]:
        """Crear un plan para lograr el objetivo"""
        tool_names = [tool.name for tool in self.tools]
        
        prompt = f"""
        Objetivo: {goal}
        Herramientas disponibles: {tool_names}
        
        Crea un plan de pasos para lograr el objetivo. 
        Responde con números y pasos específicos:
        1. [primer paso]
        2. [segundo paso]
        ...
        """
        
        plan_text = self.llm.predict(prompt)
        self.plan = [step.strip() for step in plan_text.split('\n') if step.strip()]
        return self.plan
    
    def execute_plan(self, goal: str) -> List[str]:
        """Ejecutar el plan paso a paso"""
        print(f"🎯 Objetivo: {goal}")
        
        # Crear plan
        plan = self.create_plan(goal)
        print(f"📋 Plan creado: {len(plan)} pasos")
        
        results = []
        for i, step in enumerate(plan, 1):
            print(f"\n📝 Paso {i}: {step}")
            
            # Ejecutar paso
            result = self.execute_step(step)
            results.append(result)
            print(f"✅ Resultado: {result}")
        
        return results
    
    def execute_step(self, step: str) -> str:
        """Ejecutar un paso individual"""
        if "buscar" in step.lower() or "información" in step.lower():
            return f"Búsqueda web: {step}"
        elif "calcular" in step.lower() or any(op in step for op in ['+', '-', '*', '/']):
            return f"Cálculo: {step}"
        elif "clima" in step.lower() or "tiempo" in step.lower():
            return "Clima: Soleado, 25°C"
        else:
            return f"Paso ejecutado: {step}"


# Herramientas de ejemplo
def search_web(query: str) -> str:
    """Buscar información en la web"""
    return f"Resultados de búsqueda para: {query}"

def calculate(expression: str) -> str:
    """Realizar cálculos matemáticos"""
    try:
        return str(eval(expression))
    except:
        return "Error en el cálculo"

def get_weather(city: str) -> str:
    """Obtener información del clima"""
    return f"Clima en {city}: Soleado, 25°C"


class Tool:
    """Clase simple para representar herramientas"""
    
    def __init__(self, name: str, func, description: str):
        self.name = name
        self.func = func
        self.description = description


def create_basic_tools() -> List[Tool]:
    """Crear herramientas básicas para el agente"""
    return [
        Tool(
            name="search_web",
            func=search_web,
            description="Buscar información en internet"
        ),
        Tool(
            name="calculate",
            func=calculate,
            description="Realizar cálculos matemáticos"
        ),
        Tool(
            name="get_weather",
            func=get_weather,
            description="Obtener información del clima"
        )
    ]


def demo_agent_fundamentals():
    """Demostración de los conceptos fundamentales de agentes"""
    print("🤖 DEMOSTRACIÓN: Fundamentos de Agentes LLM")
    print("=" * 50)
    
    # Simular LLM (en un caso real usarías OpenAI, etc.)
    class MockLLM:
        def predict(self, prompt: str) -> str:
            if "herramienta" in prompt.lower():
                return "search_web"
            elif "plan" in prompt.lower():
                return "1. Buscar información\n2. Analizar datos\n3. Generar resumen"
            else:
                return "respond"
    
    llm = MockLLM()
    tools = create_basic_tools()
    
    # 1. Agente Simple
    print("\n1️⃣ Agente Simple (Ciclo Percepción-Decisión-Acción):")
    simple_agent = SimpleAgent(llm)
    result = simple_agent.run("¿Qué es la inteligencia artificial?")
    
    # 2. Agente Reactivo
    print("\n2️⃣ Agente Reactivo:")
    reactive_agent = ReactiveAgent(llm, tools)
    result = reactive_agent.respond("¿Cuál es el clima en Madrid?")
    print(f"Respuesta: {result}")
    
    # 3. Agente con Planificación
    print("\n3️⃣ Agente con Planificación:")
    planning_agent = PlanningAgent(llm, tools)
    planning_agent.execute_plan("Investigar sobre machine learning")


if __name__ == "__main__":
    demo_agent_fundamentals() 