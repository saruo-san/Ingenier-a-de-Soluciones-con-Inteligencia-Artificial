"""
IL2.2: Sistemas de Memoria para Agentes LLM
==========================================

Este módulo explora diferentes tipos de sistemas de memoria para agentes LLM,
incluyendo memoria conversacional, de trabajo, episódica y semántica.
"""

import json
import time
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib


@dataclass
class MemoryItem:
    """Elemento de memoria"""
    content: str
    timestamp: float
    memory_type: str
    importance: float = 1.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.timestamp is None:
            self.timestamp = time.time()


class MemorySystem(ABC):
    """Sistema de memoria base"""
    
    def __init__(self, name: str):
        self.name = name
        self.memories: List[MemoryItem] = []
        self.max_memories: int = 1000
    
    @abstractmethod
    def store(self, content: str, memory_type: str = "general", **kwargs) -> str:
        """Almacenar memoria"""
        pass
    
    @abstractmethod
    def retrieve(self, query: str, limit: int = 5) -> List[MemoryItem]:
        """Recuperar memorias relevantes"""
        pass
    
    def clear(self):
        """Limpiar todas las memorias"""
        self.memories.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de memoria"""
        return {
            "total_memories": len(self.memories),
            "memory_types": self._get_memory_type_counts(),
            "oldest_memory": min([m.timestamp for m in self.memories]) if self.memories else None,
            "newest_memory": max([m.timestamp for m in self.memories]) if self.memories else None
        }
    
    def _get_memory_type_counts(self) -> Dict[str, int]:
        """Contar memorias por tipo"""
        counts = {}
        for memory in self.memories:
            counts[memory.memory_type] = counts.get(memory.memory_type, 0) + 1
        return counts


class SimpleMemorySystem(MemorySystem):
    """Sistema de memoria simple basado en lista"""
    
    def store(self, content: str, memory_type: str = "general", importance: float = 1.0, **kwargs) -> str:
        """Almacenar memoria"""
        memory = MemoryItem(
            content=content,
            timestamp=time.time(),
            memory_type=memory_type,
            importance=importance,
            metadata=kwargs
        )
        
        self.memories.append(memory)
        
        # Mantener límite de memorias
        if len(self.memories) > self.max_memories:
            # Eliminar la memoria más antigua
            self.memories.pop(0)
        
        return f"Memoria almacenada: {content[:50]}..."
    
    def retrieve(self, query: str, limit: int = 5) -> List[MemoryItem]:
        """Recuperar memorias relevantes (búsqueda simple)"""
        # Búsqueda simple por palabras clave
        query_words = query.lower().split()
        relevant_memories = []
        
        for memory in reversed(self.memories):  # Más recientes primero
            content_lower = memory.content.lower()
            relevance_score = sum(1 for word in query_words if word in content_lower)
            
            if relevance_score > 0:
                relevant_memories.append((memory, relevance_score))
        
        # Ordenar por relevancia y importancia
        relevant_memories.sort(key=lambda x: (x[1], x[0].importance), reverse=True)
        
        return [memory for memory, _ in relevant_memories[:limit]]


if __name__ == "__main__":
    # Demostración simple
    memory = SimpleMemorySystem("test")
    memory.store("Hola mundo", "test")
    print("Memoria creada exitosamente") 