"""
IL3.3: Seguridad y Ética en Agentes de IA
========================================
Ejemplo de recomendaciones básicas de seguridad y ética.
"""

def safe_eval(expression):
    """Evalúa solo expresiones matemáticas seguras."""
    allowed = set('0123456789+-*/(). ')
    if not set(expression) <= allowed:
        return "Expresión no permitida."
    try:
        return str(eval(expression))
    except Exception:
        return "Error en la expresión."

class EthicalAgent:
    def answer(self, question):
        if "hackear" in question.lower():
            return "No puedo ayudar con esa solicitud."
        return "Solo respondo preguntas apropiadas."

if __name__ == "__main__":
    print(safe_eval("2+2*2"))
    agent = EthicalAgent()
    print(agent.answer("¿Cómo hackear un sistema?")) 