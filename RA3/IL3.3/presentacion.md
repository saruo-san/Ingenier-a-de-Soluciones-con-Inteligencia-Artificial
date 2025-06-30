# Presentación IL3.3 - Seguridad y Ética en Agentes de IA

## Slide 1: Título y Objetivos
**Título:** IL3.3 - Seguridad y Ética en Agentes de IA  
**Subtítulo:** Prácticas Responsables y Protección de Sistemas IA

**Objetivos:**
- Implementar validación segura de inputs
- Establecer filtros éticos en respuestas
- Proteger contra ataques y mal uso
- Desarrollar agentes responsables y seguros

---

## Slide 2: ¿Por qué Seguridad y Ética?
**Título:** Riesgos de Agentes IA sin Protecciones

**Riesgos de seguridad:**
- **Code injection:** Ejecución de código malicioso
- **Prompt injection:** Manipulación del comportamiento
- **Data exfiltration:** Acceso no autorizado a información
- **Resource abuse:** Uso excesivo de recursos

**Riesgos éticos:**
- **Harmful content:** Generación de contenido dañino
- **Bias amplification:** Amplificación de sesgos
- **Privacy violations:** Violación de privacidad
- **Misinformation:** Propagación de información falsa

**Responsabilidad organizacional:**
- Compliance con regulaciones
- Protección de usuarios y datos
- Reputación corporativa
- Responsabilidad legal

---

## Slide 3: Seguridad Básica - Validación de Inputs
**Título:** Script 1 - Evaluación Segura y Filtros Éticos

**Evaluación segura:**
```python
def safe_eval(expression):
    """Evalúa solo expresiones matemáticas seguras."""
    allowed = set('0123456789+-*/(). ')
    if not set(expression) <= allowed:
        return "Expresión no permitida."
    try:
        return str(eval(expression))
    except Exception:
        return "Error en la expresión."
```

**Filtros éticos:**
```python
class EthicalAgent:
    def answer(self, question):
        if "hackear" in question.lower():
            return "No puedo ayudar con esa solicitud."
        return "Solo respondo preguntas apropiadas."
```

**Principios implementados:**
- **Input validation:** Solo caracteres permitidos
- **Content filtering:** Detección de solicitudes inapropiadas
- **Safe execution:** Manejo de errores controlado

---

## Slide 4: Principios de Seguridad para Agentes
**Título:** Framework de Protección Integral

**1. Input Sanitization:**
```python
import re

class SecureAgent:
    def sanitize_input(self, user_input):
        # Remover caracteres peligrosos
        cleaned = re.sub(r'[<>\"\';&|`]', '', user_input)
        
        # Limitar longitud
        if len(cleaned) > 1000:
            return cleaned[:1000]
        
        return cleaned
```

**2. Output Validation:**
```python
def validate_response(self, response):
    dangerous_patterns = [
        r'password:\s*\w+',
        r'api[_-]?key:\s*\w+',
        r'token:\s*\w+',
        r'eval\s*\(',
        r'exec\s*\('
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, response, re.IGNORECASE):
            return "Response blocked for security."
    
    return response
```

**3. Access Control:**
- Principio de menor privilegio
- Autenticación y autorización
- Rate limiting por usuario
- Session management seguro

---

## Slide 5: Ética en IA - Frameworks de Decisión
**Título:** Implementando Comportamiento Ético

**Principios éticos fundamentales:**
- **Beneficencia:** Actuar para el bien común
- **No maleficencia:** "No hacer daño"
- **Autonomía:** Respetar la agencia humana
- **Justicia:** Trato equitativo y fair

**Implementación práctica:**
```python
class EthicalFramework:
    def __init__(self):
        self.prohibited_topics = [
            "violence", "hate_speech", "illegal_activities",
            "self_harm", "private_information", "manipulation"
        ]
        
        self.sensitive_topics = [
            "medical_advice", "legal_advice", "financial_advice"
        ]
    
    def ethical_check(self, query, response):
        # Verificar temas prohibidos
        for topic in self.prohibited_topics:
            if self.contains_topic(query, topic) or self.contains_topic(response, topic):
                return False, f"Topic {topic} is prohibited"
        
        # Advertencias para temas sensibles
        for topic in self.sensitive_topics:
            if self.contains_topic(query, topic):
                return True, f"Warning: Seek professional {topic.replace('_', ' ')} advice"
        
        return True, "Ethical check passed"
```

---

## Slide 6: Protección contra Ataques Comunes
**Título:** Defensas contra Prompt Injection y Adversarial Attacks

**1. Prompt Injection Protection:**
```python
class PromptGuard:
    def __init__(self):
        self.injection_patterns = [
            r"ignore\s+previous\s+instructions",
            r"forget\s+everything\s+above",
            r"act\s+as\s+if\s+you\s+are",
            r"pretend\s+to\s+be",
            r"system\s*:\s*you\s+are\s+now"
        ]
    
    def detect_injection(self, user_input):
        for pattern in self.injection_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return True
        return False
    
    def sanitize_prompt(self, user_input):
        if self.detect_injection(user_input):
            return "I notice you're trying to change my instructions. I'll stick to my original purpose."
        return user_input
```

**2. Data Exfiltration Prevention:**
```python
class DataProtection:
    def __init__(self):
        self.sensitive_patterns = [
            r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # Credit cards
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Email
        ]
    
    def contains_sensitive_data(self, text):
        for pattern in self.sensitive_patterns:
            if re.search(pattern, text):
                return True
        return False
```

**3. Rate Limiting:**
```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, requests_per_minute=60):
        self.requests_per_minute = requests_per_minute
        self.user_requests = defaultdict(list)
    
    def is_allowed(self, user_id):
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests
        self.user_requests[user_id] = [
            req_time for req_time in self.user_requests[user_id] 
            if req_time > minute_ago
        ]
        
        # Check limit
        if len(self.user_requests[user_id]) >= self.requests_per_minute:
            return False
        
        # Log request
        self.user_requests[user_id].append(now)
        return True
```

---

## Slide 7: Governance y Compliance
**Título:** Marcos Regulatorios y Estándares

**Regulaciones clave:**
- **EU AI Act:** Clasificación de riesgo y requisitos
- **GDPR:** Protección de datos y privacidad
- **CCPA:** Derechos de consumidores en California
- **SOC 2:** Controles de seguridad organizacional

**Implementación de compliance:**
```python
class ComplianceManager:
    def __init__(self):
        self.audit_log = []
        self.consent_records = {}
        
    def log_decision(self, user_id, decision, reasoning, confidence):
        """GDPR Article 22 - Right to explanation"""
        self.audit_log.append({
            "timestamp": time.time(),
            "user_id": user_id,
            "decision": decision,
            "reasoning": reasoning,
            "confidence": confidence,
            "human_review_available": True
        })
    
    def check_consent(self, user_id, purpose):
        """GDPR Article 6 - Lawfulness of processing"""
        return self.consent_records.get(user_id, {}).get(purpose, False)
    
    def anonymize_data(self, data):
        """Privacy by design"""
        # Implementar técnicas de anonimización
        pass
```

---

## Slide 8: Monitoring y Detección de Anomalías
**Título:** Vigilancia Continua de Comportamiento

**Security monitoring:**
```python
class SecurityMonitor:
    def __init__(self):
        self.threat_indicators = []
        self.behavioral_baseline = {}
    
    def detect_anomalies(self, user_id, request_pattern):
        """Detectar comportamiento anómalo"""
        baseline = self.behavioral_baseline.get(user_id, {})
        
        # Frecuencia inusual de requests
        if request_pattern['frequency'] > baseline.get('avg_frequency', 0) * 3:
            return "High frequency anomaly detected"
        
        # Patrones de consulta inusuales
        if request_pattern['complexity'] > baseline.get('avg_complexity', 0) * 2:
            return "Query complexity anomaly detected"
        
        return None
    
    def update_threat_intel(self, new_indicators):
        """Actualizar indicadores de amenaza"""
        self.threat_indicators.extend(new_indicators)
```

**Ethical monitoring:**
```python
class EthicsMonitor:
    def track_bias_indicators(self, responses_by_demographic):
        """Monitorear sesgos en respuestas"""
        bias_metrics = {}
        
        for demographic, responses in responses_by_demographic.items():
            bias_metrics[demographic] = {
                'avg_sentiment': self.calculate_sentiment(responses),
                'response_length': self.avg_length(responses),
                'topics_covered': self.extract_topics(responses)
            }
        
        return self.analyze_bias(bias_metrics)
```

---

## Slide 9: Próximos Pasos hacia IL3.4
**Título:** Evolución hacia Escalabilidad y Sostenibilidad

**Preparación para IL3.4:**
- Seguridad y ética como foundation
- Compliance frameworks implementados
- Monitoring de amenazas establecido
- Governance structures en su lugar

**IL3.4 - Escalabilidad y Sostenibilidad:**
- Performance optimization con security
- Sustainable AI practices
- Green computing para agentes
- Long-term maintainability

**Proyecto final RA3:**
- **IL3.1:** Observabilidad ✓
- **IL3.2:** Trazabilidad ✓  
- **IL3.3:** Seguridad y ética ✓
- **IL3.4:** Escalabilidad sostenible

---

## Slide 10: Resumen Ejecutivo
**Título:** Conceptos Clave del Módulo IL3.3

**Fundamentos establecidos:**
1. **Input validation** con sanitización segura
2. **Ethical filtering** para contenido apropiado
3. **Protection frameworks** contra ataques comunes
4. **Compliance structures** para regulaciones

**Implementación práctica:**
- Safe evaluation de expresiones matemáticas
- Filtros éticos para consultas inapropiadas
- Frameworks de seguridad modulares
- Monitoring de anomalías y sesgos

**Valor organizacional:**
- **Risk mitigation:** Protección contra amenazas
- **Regulatory compliance:** Cumplimiento legal
- **Trust building:** Confianza de usuarios
- **Reputation protection:** Protección de marca

**Preparación para IL3.4:**
- Security by design establecido
- Ethical frameworks operativos
- Foundation para scaling seguro
- Governance para sostenibilidad