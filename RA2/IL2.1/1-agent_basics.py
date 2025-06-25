"""
IL2.1: Agente Básico
====================
Ejemplo de un agente simple que responde a una pregunta.
"""

def simple_agent(question):
    """Agente que responde a preguntas simples."""
    if "nombre" in question.lower():
        return "Mi nombre es AgenteSimple."
    elif "suma" in question.lower():
        return "La suma de 2 + 2 es 4."
    else:
        return "No sé la respuesta, pero puedo aprender."

if __name__ == "__main__":
    print(simple_agent("¿Cuál es tu nombre?"))
    print(simple_agent("¿Cuánto es la suma de 2 + 2?"))
    print(simple_agent("¿Qué es inteligencia artificial?")) 