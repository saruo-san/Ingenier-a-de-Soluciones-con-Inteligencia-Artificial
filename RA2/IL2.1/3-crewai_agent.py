"""
IL2.1: Agente con CrewAI (Básico)
=================================
Ejemplo mínimo de uso de CrewAI para crear un agente.
"""

# Requiere: pip install crewai
from crewai import Agent, Task, Crew

# Define un agente
agente = Agent(
    role="Asistente",
    goal="Responder preguntas simples",
    backstory="Eres un asistente útil y directo."
)

tarea = Task(
    description="Responde: ¿Cuál es la capital de Francia?",
    agent=agente
)

crew = Crew(
    agents=[agente],
    tasks=[tarea],
    verbose=True
)

if __name__ == "__main__":
    print(crew.kickoff()) 