"""
IL2.1: Agente con LangChain (Básico)
====================================
Ejemplo mínimo de uso de LangChain para crear un agente.
"""

# Requiere: pip install langchain openai
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool, AgentType
import os

# Configura tu API key de OpenAI
os.environ["OPENAI_API_KEY"] = "sk-..."

# Define una herramienta simple
herramienta = Tool(
    name="Calculadora",
    func=lambda x: str(eval(x)),
    description="Realiza cálculos matemáticos simples."
)

# Inicializa el LLM y el agente
llm = OpenAI(temperature=0)
agente = initialize_agent(
    tools=[herramienta],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    print(agente.run("¿Cuánto es 5 * 7?")) 