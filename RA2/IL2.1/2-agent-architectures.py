"""
IL2.1: Arquitecturas de Agentes
==============================

Este módulo explora diferentes patrones arquitectónicos para agentes LLM,
incluyendo arquitecturas monolíticas, modulares, y basadas en eventos.
"""

from typing import Dict, List, Any, Callable
from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass
from enum import Enum


class AgentState(Enum):
    """Estados posibles de un agente"""
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    WAITING = "waiting"
    ERROR = "error"


@dataclass
class AgentEvent:
    """Evento del agente"""
    type: str
    data: Dict[str, Any]
    timestamp: float


class AgentArchitecture(ABC):
    """Clase base para arquitecturas de agentes"""
    
    def __init__(self, name: str):
        self.name = name
        self.state = AgentState.IDLE
        self.memory = []
        self.events = []
    
    @abstractmethod
    def process_input(self, input_data: Any) -> Any:
        """Procesar entrada según la arquitectura"""
        pass
    
    def add_event(self, event_type: str, data: Dict[str, Any]):
        """Agregar evento al historial"""
        import time
        event = AgentEvent(
            type=event_type,
            data=data,
            timestamp=time.time()
        )
        self.events.append(event)


class MonolithicArchitecture(AgentArchitecture):
    """
    Arquitectura monolítica: todo el procesamiento en un solo componente
    """
    
    def __init__(self, name: str, llm, tools: List[Any]):
        super().__init__(name)
        self.llm = llm
        self.tools = tools
    
    def process_input(self, input_data: str) -> str:
        """Procesar entrada de forma monolítica"""
        self.state = AgentState.THINKING
        self.add_event("input_received", {"input": input_data})
        
        # Todo el procesamiento en un solo lugar
        response = self.llm.predict(f"Procesa: {input_data}")
        
        self.state = AgentState.ACTING
        self.add_event("response_generated", {"response": response})
        
        self.state = AgentState.IDLE
        return response


class ModularArchitecture(AgentArchitecture):
    """
    Arquitectura modular: componentes separados para diferentes funciones
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        self.modules = {}
        self.pipeline = []
    
    def add_module(self, name: str, module: Callable):
        """Agregar módulo a la arquitectura"""
        self.modules[name] = module
        self.pipeline.append(name)
    
    def process_input(self, input_data: str) -> str:
        """Procesar entrada a través de módulos"""
        self.state = AgentState.THINKING
        self.add_event("input_received", {"input": input_data})
        
        current_data = input_data
        
        # Procesar a través de cada módulo en el pipeline
        for module_name in self.pipeline:
            module = self.modules[module_name]
            current_data = module(current_data)
            self.add_event("module_processed", {
                "module": module_name,
                "output": current_data
            })
        
        self.state = AgentState.IDLE
        return current_data


class EventDrivenArchitecture(AgentArchitecture):
    """
    Arquitectura basada en eventos: componentes se comunican mediante eventos
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        self.event_handlers = {}
        self.event_queue = []
    
    def register_handler(self, event_type: str, handler: Callable):
        """Registrar manejador de eventos"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emitir evento"""
        self.add_event(event_type, data)
        self.event_queue.append((event_type, data))
    
    def process_events(self):
        """Procesar cola de eventos"""
        while self.event_queue:
            event_type, data = self.event_queue.pop(0)
            if event_type in self.event_handlers:
                for handler in self.event_handlers[event_type]:
                    handler(data)
    
    def process_input(self, input_data: str) -> str:
        """Procesar entrada mediante eventos"""
        self.state = AgentState.THINKING
        
        # Emitir evento de entrada
        self.emit_event("input_received", {"input": input_data})
        
        # Procesar eventos
        self.process_events()
        
        # Emitir evento de respuesta
        response = f"Procesado: {input_data}"
        self.emit_event("response_ready", {"response": response})
        
        self.state = AgentState.IDLE
        return response


class LayeredArchitecture(AgentArchitecture):
    """
    Arquitectura en capas: diferentes niveles de abstracción
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        self.layers = {
            "presentation": [],
            "business": [],
            "data": []
        }
    
    def add_to_layer(self, layer: str, component: Callable):
        """Agregar componente a una capa"""
        if layer in self.layers:
            self.layers[layer].append(component)
    
    def process_input(self, input_data: str) -> str:
        """Procesar entrada a través de capas"""
        self.state = AgentState.THINKING
        self.add_event("input_received", {"input": input_data})
        
        current_data = input_data
        
        # Procesar capa de presentación
        for component in self.layers["presentation"]:
            current_data = component(current_data)
        
        # Procesar capa de negocio
        for component in self.layers["business"]:
            current_data = component(current_data)
        
        # Procesar capa de datos
        for component in self.layers["data"]:
            current_data = component(current_data)
        
        self.state = AgentState.IDLE
        return current_data


class MicroservicesArchitecture(AgentArchitecture):
    """
    Arquitectura de microservicios: servicios independientes
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        self.services = {}
        self.service_dependencies = {}
    
    def add_service(self, name: str, service: Callable, dependencies: List[str] = None):
        """Agregar servicio"""
        self.services[name] = service
        self.service_dependencies[name] = dependencies or []
    
    def execute_service(self, service_name: str, data: Any) -> Any:
        """Ejecutar servicio con sus dependencias"""
        # Verificar dependencias
        for dep in self.service_dependencies[service_name]:
            if dep in self.services:
                data = self.execute_service(dep, data)
        
        # Ejecutar servicio
        return self.services[service_name](data)
    
    def process_input(self, input_data: str) -> str:
        """Procesar entrada a través de servicios"""
        self.state = AgentState.THINKING
        self.add_event("input_received", {"input": input_data})
        
        current_data = input_data
        
        # Ejecutar servicios principales
        for service_name in self.services:
            if not self.service_dependencies[service_name]:  # Servicios sin dependencias
                current_data = self.execute_service(service_name, current_data)
        
        self.state = AgentState.IDLE
        return current_data


# Componentes de ejemplo para las arquitecturas
def text_preprocessor(text: str) -> str:
    """Preprocesar texto"""
    return text.lower().strip()

def sentiment_analyzer(text: str) -> str:
    """Analizar sentimiento"""
    return f"Sentimiento: positivo en '{text}'"

def content_generator(text: str) -> str:
    """Generar contenido"""
    return f"Contenido generado para: {text}"

def data_validator(data: str) -> str:
    """Validar datos"""
    return f"Datos validados: {data}"

def response_formatter(response: str) -> str:
    """Formatear respuesta"""
    return f"Respuesta formateada: {response}"


def demo_architectures():
    """Demostración de diferentes arquitecturas"""
    print("🏗️ DEMOSTRACIÓN: Arquitecturas de Agentes")
    print("=" * 50)
    
    # Simular LLM
    class MockLLM:
        def predict(self, prompt: str) -> str:
            return f"Procesado: {prompt}"
    
    llm = MockLLM()
    
    # 1. Arquitectura Monolítica
    print("\n1️⃣ Arquitectura Monolítica:")
    monolithic = MonolithicArchitecture("MonolithicAgent", llm, [])
    result = monolithic.process_input("Hola mundo")
    print(f"Resultado: {result}")
    print(f"Eventos: {len(monolithic.events)}")
    
    # 2. Arquitectura Modular
    print("\n2️⃣ Arquitectura Modular:")
    modular = ModularArchitecture("ModularAgent")
    modular.add_module("preprocessor", text_preprocessor)
    modular.add_module("analyzer", sentiment_analyzer)
    modular.add_module("generator", content_generator)
    result = modular.process_input("Texto de prueba")
    print(f"Resultado: {result}")
    
    # 3. Arquitectura Basada en Eventos
    print("\n3️⃣ Arquitectura Basada en Eventos:")
    event_driven = EventDrivenArchitecture("EventDrivenAgent")
    
    def input_handler(data):
        print(f"  📥 Procesando entrada: {data['input']}")
    
    def response_handler(data):
        print(f"  📤 Respuesta lista: {data['response']}")
    
    event_driven.register_handler("input_received", input_handler)
    event_driven.register_handler("response_ready", response_handler)
    result = event_driven.process_input("Evento de prueba")
    print(f"Resultado: {result}")
    
    # 4. Arquitectura en Capas
    print("\n4️⃣ Arquitectura en Capas:")
    layered = LayeredArchitecture("LayeredAgent")
    layered.add_to_layer("presentation", text_preprocessor)
    layered.add_to_layer("business", sentiment_analyzer)
    layered.add_to_layer("data", data_validator)
    result = layered.process_input("Texto en capas")
    print(f"Resultado: {result}")
    
    # 5. Arquitectura de Microservicios
    print("\n5️⃣ Arquitectura de Microservicios:")
    microservices = MicroservicesArchitecture("MicroservicesAgent")
    microservices.add_service("validator", data_validator)
    microservices.add_service("analyzer", sentiment_analyzer, ["validator"])
    microservices.add_service("formatter", response_formatter, ["analyzer"])
    result = microservices.process_input("Servicio de prueba")
    print(f"Resultado: {result}")


def compare_architectures():
    """Comparar características de las arquitecturas"""
    print("\n📊 COMPARACIÓN DE ARQUITECTURAS")
    print("=" * 50)
    
    comparison = {
        "Monolítica": {
            "Complejidad": "Baja",
            "Mantenimiento": "Difícil",
            "Escalabilidad": "Limitada",
            "Flexibilidad": "Baja",
            "Casos de uso": "Aplicaciones simples"
        },
        "Modular": {
            "Complejidad": "Media",
            "Mantenimiento": "Fácil",
            "Escalabilidad": "Media",
            "Flexibilidad": "Alta",
            "Casos de uso": "Aplicaciones medianas"
        },
        "Basada en Eventos": {
            "Complejidad": "Alta",
            "Mantenimiento": "Media",
            "Escalabilidad": "Alta",
            "Flexibilidad": "Muy alta",
            "Casos de uso": "Sistemas distribuidos"
        },
        "En Capas": {
            "Complejidad": "Media",
            "Mantenimiento": "Fácil",
            "Escalabilidad": "Media",
            "Flexibilidad": "Media",
            "Casos de uso": "Aplicaciones empresariales"
        },
        "Microservicios": {
            "Complejidad": "Muy alta",
            "Mantenimiento": "Difícil",
            "Escalabilidad": "Muy alta",
            "Flexibilidad": "Muy alta",
            "Casos de uso": "Sistemas complejos"
        }
    }
    
    for arch, features in comparison.items():
        print(f"\n🏗️ {arch}:")
        for feature, value in features.items():
            print(f"  {feature}: {value}")


if __name__ == "__main__":
    demo_architectures()
    compare_architectures() 