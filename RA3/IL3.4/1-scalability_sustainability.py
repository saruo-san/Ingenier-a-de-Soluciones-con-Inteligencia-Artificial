"""
IL3.4: Escalabilidad y Sostenibilidad
====================================
Recomendaciones básicas para escalar y mantener agentes de IA.
"""

# Recomendaciones:
# - Usa logs para monitorear el rendimiento.
# - Divide el sistema en componentes pequeños (microservicios).
# - Usa colas de mensajes para tareas concurrentes.
# - Documenta y automatiza los despliegues.
# - Monitorea el consumo de recursos y ajusta según demanda.

class ScalableAgent:
    def process(self, data):
        # Simula procesamiento escalable
        return f"Procesando: {data}"

if __name__ == "__main__":
    agent = ScalableAgent()
    print(agent.process("Tarea 1"))
    print(agent.process("Tarea 2")) 