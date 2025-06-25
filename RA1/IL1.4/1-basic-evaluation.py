import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any
import numpy as np
from openai import OpenAI

class LLMEvaluator:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("GITHUB_BASE_URL", "https://models.inference.ai.azure.com"),
            api_key=os.getenv("GITHUB_TOKEN")
        )
        self.evaluation_results = []
    
    def evaluate_relevance(self, query: str, response: str) -> Dict[str, Any]:
        """Evalúa qué tan relevante es la respuesta para la consulta"""
        eval_prompt = f"""Evalúa la relevancia de la respuesta para la consulta en una escala del 1-10.

Consulta: {query}

Respuesta: {response}

Criterios de evaluación:
- 1-3: Respuesta no relacionada o completamente irrelevante
- 4-6: Respuesta parcialmente relevante, aborda algunos aspectos
- 7-8: Respuesta relevante, aborda la mayoría de aspectos importantes
- 9-10: Respuesta muy relevante, aborda completamente la consulta

Proporciona:
1. Puntuación (1-10)
2. Justificación breve

Formato de respuesta:
Puntuación: [número]
Justificación: [explicación]"""

        try:
            response_eval = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": eval_prompt}],
                temperature=0.1,
                max_tokens=200
            )
            
            content = response_eval.choices[0].message.content
            lines = content.strip().split('\n')
            
            score = None
            justification = ""
            
            for line in lines:
                if line.startswith("Puntuación:"):
                    score = float(line.split(":")[1].strip())
                elif line.startswith("Justificación:"):
                    justification = line.split(":", 1)[1].strip()
            
            return {
                "metric": "relevance",
                "score": score or 5.0,
                "justification": justification,
                "max_score": 10.0
            }
        except Exception as e:
            return {
                "metric": "relevance",
                "score": 0.0,
                "justification": f"Error en evaluación: {str(e)}",
                "max_score": 10.0
            }
    
    def evaluate_faithfulness(self, context: str, response: str) -> Dict[str, Any]:
        """Evalúa si la respuesta es fiel al contexto proporcionado"""
        eval_prompt = f"""Evalúa si la respuesta es fiel al contexto proporcionado en una escala del 1-10.

Contexto:
{context}

Respuesta:
{response}

Criterios de evaluación:
- 1-3: Respuesta contradice el contexto o inventa información
- 4-6: Respuesta parcialmente basada en el contexto
- 7-8: Respuesta mayormente fiel al contexto
- 9-10: Respuesta completamente fiel, no agrega información externa

Proporciona:
1. Puntuación (1-10)
2. Justificación breve

Formato de respuesta:
Puntuación: [número]
Justificación: [explicación]"""

        try:
            response_eval = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": eval_prompt}],
                temperature=0.1,
                max_tokens=200
            )
            
            content = response_eval.choices[0].message.content
            lines = content.strip().split('\n')
            
            score = None
            justification = ""
            
            for line in lines:
                if line.startswith("Puntuación:"):
                    score = float(line.split(":")[1].strip())
                elif line.startswith("Justificación:"):
                    justification = line.split(":", 1)[1].strip()
            
            return {
                "metric": "faithfulness",
                "score": score or 5.0,
                "justification": justification,
                "max_score": 10.0
            }
        except Exception as e:
            return {
                "metric": "faithfulness",
                "score": 0.0,
                "justification": f"Error en evaluación: {str(e)}",
                "max_score": 10.0
            }
    
    def evaluate_completeness(self, query: str, response: str) -> Dict[str, Any]:
        """Evalúa qué tan completa es la respuesta"""
        eval_prompt = f"""Evalúa la completitud de la respuesta en una escala del 1-10.

Consulta: {query}

Respuesta: {response}

Criterios de evaluación:
- 1-3: Respuesta muy incompleta, falta información esencial
- 4-6: Respuesta parcialmente completa, algunos aspectos importantes
- 7-8: Respuesta bastante completa, cubre la mayoría de aspectos
- 9-10: Respuesta muy completa, cubre todos los aspectos importantes

Proporciona:
1. Puntuación (1-10)
2. Justificación breve

Formato de respuesta:
Puntuación: [número]
Justificación: [explicación]"""

        try:
            response_eval = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": eval_prompt}],
                temperature=0.1,
                max_tokens=200
            )
            
            content = response_eval.choices[0].message.content
            lines = content.strip().split('\n')
            
            score = None
            justification = ""
            
            for line in lines:
                if line.startswith("Puntuación:"):
                    score = float(line.split(":")[1].strip())
                elif line.startswith("Justificación:"):
                    justification = line.split(":", 1)[1].strip()
            
            return {
                "metric": "completeness",
                "score": score or 5.0,
                "justification": justification,
                "max_score": 10.0
            }
        except Exception as e:
            return {
                "metric": "completeness",
                "score": 0.0,
                "justification": f"Error en evaluación: {str(e)}",
                "max_score": 10.0
            }
    
    def evaluate_clarity(self, response: str) -> Dict[str, Any]:
        """Evalúa la claridad y legibilidad de la respuesta"""
        eval_prompt = f"""Evalúa la claridad y legibilidad de la respuesta en una escala del 1-10.

Respuesta: {response}

Criterios de evaluación:
- 1-3: Respuesta confusa, difícil de entender
- 4-6: Respuesta parcialmente clara, algunos aspectos confusos
- 7-8: Respuesta clara, fácil de entender
- 9-10: Respuesta muy clara, excelente comunicación

Proporciona:
1. Puntuación (1-10)
2. Justificación breve

Formato de respuesta:
Puntuación: [número]
Justificación: [explicación]"""

        try:
            response_eval = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": eval_prompt}],
                temperature=0.1,
                max_tokens=200
            )
            
            content = response_eval.choices[0].message.content
            lines = content.strip().split('\n')
            
            score = None
            justification = ""
            
            for line in lines:
                if line.startswith("Puntuación:"):
                    score = float(line.split(":")[1].strip())
                elif line.startswith("Justificación:"):
                    justification = line.split(":", 1)[1].strip()
            
            return {
                "metric": "clarity",
                "score": score or 5.0,
                "justification": justification,
                "max_score": 10.0
            }
        except Exception as e:
            return {
                "metric": "clarity",
                "score": 0.0,
                "justification": f"Error en evaluación: {str(e)}",
                "max_score": 10.0
            }
    
    def calculate_basic_metrics(self, response: str) -> Dict[str, Any]:
        """Calcula métricas básicas de la respuesta"""
        words = response.split()
        sentences = response.split('.')
        
        return {
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "avg_words_per_sentence": len(words) / max(len([s for s in sentences if s.strip()]), 1),
            "character_count": len(response),
            "response_length_category": self._categorize_length(len(words))
        }
    
    def _categorize_length(self, word_count: int) -> str:
        """Categoriza la longitud de la respuesta"""
        if word_count < 20:
            return "muy_corta"
        elif word_count < 50:
            return "corta"
        elif word_count < 150:
            return "media"
        elif word_count < 300:
            return "larga"
        else:
            return "muy_larga"
    
    def evaluate_response(self, query: str, response: str, context: str = None) -> Dict[str, Any]:
        """Evaluación completa de una respuesta"""
        print(f"Evaluando respuesta para: {query[:50]}...")
        
        # Métricas básicas
        basic_metrics = self.calculate_basic_metrics(response)
        
        # Evaluaciones con LLM
        relevance = self.evaluate_relevance(query, response)
        completeness = self.evaluate_completeness(query, response)
        clarity = self.evaluate_clarity(response)
        
        evaluation_result = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "context": context,
            "basic_metrics": basic_metrics,
            "llm_evaluations": {
                "relevance": relevance,
                "completeness": completeness,
                "clarity": clarity
            }
        }
        
        # Si hay contexto, evaluar fidelidad
        if context:
            faithfulness = self.evaluate_faithfulness(context, response)
            evaluation_result["llm_evaluations"]["faithfulness"] = faithfulness
        
        # Calcular puntuación general
        scores = [eval_data["score"] for eval_data in evaluation_result["llm_evaluations"].values()]
        evaluation_result["overall_score"] = np.mean(scores)
        
        self.evaluation_results.append(evaluation_result)
        return evaluation_result
    
    def evaluate_dataset(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evalúa un conjunto de datos completo"""
        print(f"Evaluando dataset con {len(dataset)} elementos...")
        
        results = []
        for i, item in enumerate(dataset):
            print(f"Procesando elemento {i+1}/{len(dataset)}")
            
            query = item.get("query", "")
            response = item.get("response", "")
            context = item.get("context", None)
            
            result = self.evaluate_response(query, response, context)
            results.append(result)
        
        # Calcular estadísticas agregadas
        all_scores = [r["overall_score"] for r in results]
        
        summary = {
            "total_evaluations": len(results),
            "average_score": np.mean(all_scores),
            "median_score": np.median(all_scores),
            "std_score": np.std(all_scores),
            "min_score": np.min(all_scores),
            "max_score": np.max(all_scores),
            "evaluation_timestamp": datetime.now().isoformat(),
            "detailed_results": results
        }
        
        return summary
    
    def export_results(self, filename: str = None, format: str = "json"):
        """Exporta los resultados de evaluación"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"evaluation_results_{timestamp}"
        
        if format == "json":
            with open(f"{filename}.json", 'w', encoding='utf-8') as f:
                json.dump(self.evaluation_results, f, indent=2, ensure_ascii=False)
            print(f"Resultados exportados a {filename}.json")
        
        elif format == "csv":
            # Aplanar datos para CSV
            csv_data = []
            for result in self.evaluation_results:
                row = {
                    "timestamp": result["timestamp"],
                    "query": result["query"],
                    "response": result["response"][:100] + "...",
                    "word_count": result["basic_metrics"]["word_count"],
                    "overall_score": result["overall_score"]
                }
                
                # Agregar puntuaciones individuales
                for metric, data in result["llm_evaluations"].items():
                    row[f"{metric}_score"] = data["score"]
                
                csv_data.append(row)
            
            with open(f"{filename}.csv", 'w', newline='', encoding='utf-8') as f:
                if csv_data:
                    writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
                    writer.writeheader()
                    writer.writerows(csv_data)
            
            print(f"Resultados exportados a {filename}.csv")
    
    def print_summary(self):
        """Imprime un resumen de las evaluaciones"""
        if not self.evaluation_results:
            print("No hay resultados de evaluación disponibles.")
            return
        
        scores = [r["overall_score"] for r in self.evaluation_results]
        
        print("\n" + "="*50)
        print("RESUMEN DE EVALUACIONES")
        print("="*50)
        print(f"Total de evaluaciones: {len(self.evaluation_results)}")
        print(f"Puntuación promedio: {np.mean(scores):.2f}/10")
        print(f"Puntuación mediana: {np.median(scores):.2f}/10")
        print(f"Desviación estándar: {np.std(scores):.2f}")
        print(f"Rango: {np.min(scores):.2f} - {np.max(scores):.2f}")
        
        # Distribución por categorías
        categories = {"Excelente (9-10)": 0, "Bueno (7-8)": 0, "Regular (5-6)": 0, "Malo (1-4)": 0}
        for score in scores:
            if score >= 9:
                categories["Excelente (9-10)"] += 1
            elif score >= 7:
                categories["Bueno (7-8)"] += 1
            elif score >= 5:
                categories["Regular (5-6)"] += 1
            else:
                categories["Malo (1-4)"] += 1
        
        print("\nDistribución de puntuaciones:")
        for category, count in categories.items():
            percentage = (count / len(scores)) * 100
            print(f"  {category}: {count} ({percentage:.1f}%)")


def create_sample_dataset():
    """Crea un dataset de ejemplo para evaluación"""
    return [
        {
            "query": "¿Qué es la inteligencia artificial?",
            "response": "La inteligencia artificial (IA) es una rama de la ciencia de la computación que se enfoca en crear sistemas capaces de realizar tareas que normalmente requieren inteligencia humana, como el reconocimiento de patrones, el aprendizaje y la toma de decisiones.",
            "context": "La inteligencia artificial es una rama de la informática que busca crear máquinas capaces de realizar tareas que requieren inteligencia humana."
        },
        {
            "query": "¿Cómo funciona el machine learning?",
            "response": "El machine learning funciona mediante algoritmos que aprenden patrones de los datos sin ser programados explícitamente para cada tarea específica.",
            "context": "El machine learning es un subconjunto de la inteligencia artificial que permite a las máquinas aprender y mejorar automáticamente a partir de la experiencia."
        },
        {
            "query": "¿Qué ventajas tiene usar RAG?",
            "response": "RAG combina recuperación de información con generación de texto, permitiendo respuestas más precisas y actualizadas basadas en conocimiento específico.",
            "context": "RAG (Retrieval-Augmented Generation) combina la búsqueda de información relevante con la generación de texto para producir respuestas más precisas."
        }
    ]


def main():
    """Función principal para demostrar el sistema de evaluación"""
    print("🧪 Sistema de Evaluación Básico para LLMs")
    print("="*50)
    
    # Inicializar evaluador
    evaluator = LLMEvaluator()
    
    # Crear dataset de ejemplo
    sample_data = create_sample_dataset()
    
    print("Evaluando dataset de ejemplo...")
    
    # Evaluar dataset
    summary = evaluator.evaluate_dataset(sample_data)
    
    # Mostrar resumen
    evaluator.print_summary()
    
    # Exportar resultados
    print("\nExportando resultados...")
    evaluator.export_results("sample_evaluation", "json")
    evaluator.export_results("sample_evaluation", "csv")
    
    print("\n✅ Evaluación completada!")
    print("\nArchivos generados:")
    print("- sample_evaluation.json: Resultados detallados")
    print("- sample_evaluation.csv: Resumen en formato tabla")
    
    # Ejemplo de evaluación individual
    print("\n" + "="*50)
    print("EJEMPLO DE EVALUACIÓN INDIVIDUAL")
    print("="*50)
    
    query = "Explica qué es un transformer en deep learning"
    response = "Un transformer es una arquitectura de red neuronal que utiliza mecanismos de atención para procesar secuencias de datos de manera eficiente."
    
    result = evaluator.evaluate_response(query, response)
    
    print(f"\nConsulta: {query}")
    print(f"Respuesta: {response}")
    print(f"Puntuación general: {result['overall_score']:.2f}/10")
    print("\nPuntuaciones detalladas:")
    for metric, data in result["llm_evaluations"].items():
        print(f"  {metric.capitalize()}: {data['score']:.1f}/10 - {data['justification']}")


if __name__ == "__main__":
    main()