"""
IL2.2: Memoria Conversacional Básica
===================================
Ejemplo de cómo un agente puede recordar el último mensaje.
"""

class ConversationalAgent:
    def __init__(self):
        self.last_message = None

    def respond(self, message):
        response = f"Recibí tu mensaje: '{message}'"
        if self.last_message:
            response += f". Anteriormente me dijiste: '{self.last_message}'"
        self.last_message = message
        return response

if __name__ == "__main__":
    agent = ConversationalAgent()
    print(agent.respond("Hola agente"))
    print(agent.respond("¿Recuerdas mi saludo?")) 