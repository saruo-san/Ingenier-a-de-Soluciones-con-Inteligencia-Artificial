"""
IL3.2: Análisis de Trazabilidad y Logs
=====================================
Ejemplo de cómo analizar logs simples para trazabilidad de agentes.
"""

import logging

# Configura logging a archivo
logging.basicConfig(filename='agent.log', level=logging.INFO)

class TraceableAgent:
    def act(self, message):
        logging.info(f"Mensaje recibido: {message}")
        return f"Procesado: {message}"

if __name__ == "__main__":
    agent = TraceableAgent()
    agent.act("Mensaje 1")
    agent.act("Mensaje 2")
    # Análisis simple de logs
    with open('agent.log') as f:
        for line in f:
            print(line.strip()) 