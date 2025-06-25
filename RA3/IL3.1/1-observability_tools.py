"""
IL3.1: Herramientas de Observabilidad y Métricas
===============================================
Ejemplo de cómo agregar logs y métricas simples a un agente.
"""

import logging
import time

# Configura logging básico
logging.basicConfig(level=logging.INFO)

class Agent:
    def __init__(self):
        self.counter = 0

    def act(self, message):
        start = time.time()
        logging.info(f"Recibido mensaje: {message}")
        self.counter += 1
        response = f"Respuesta #{self.counter} a: {message}"
        duration = time.time() - start
        logging.info(f"Duración de respuesta: {duration:.4f} segundos")
        return response

if __name__ == "__main__":
    agent = Agent()
    print(agent.act("Hola"))
    print(agent.act("¿Cómo estás?")) 