"""
IL2.2: Integración de Herramienta Externa
=========================================
Ejemplo de cómo un agente puede usar una función externa (simulada).
"""

def get_weather(city):
    """Simula obtener el clima de una ciudad."""
    return f"El clima en {city} es soleado."

class ToolAgent:
    def ask_weather(self, city):
        return get_weather(city)

if __name__ == "__main__":
    agent = ToolAgent()
    print(agent.ask_weather("Madrid")) 