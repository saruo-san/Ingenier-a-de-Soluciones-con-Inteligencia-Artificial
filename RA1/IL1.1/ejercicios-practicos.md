# Ejercicios Prácticos IL1.1 - LLMs y Conexiones API

## Objetivo General
Consolidar los conocimientos adquiridos en IL1.1 mediante ejercicios progresivos que integren todos los conceptos: APIs directas, LangChain, streaming, memoria y mejores prácticas.

---

## 🏗️ Ejercicios Básicos (Individual)

### Ejercicio 1: Configuración Multi-Proveedor
**Objetivo**: Dominar la configuración de diferentes proveedores de LLMs

**Tareas**:
1. Configura conexiones a al menos 2 proveedores diferentes
2. Implementa un sistema de fallback entre proveedores
3. Compara respuestas del mismo prompt entre proveedores
4. Documenta diferencias en formato, velocidad y calidad

**Entregable**: Script Python con configuración robusta y reporte comparativo

**Criterios de Evaluación**:
- ✅ Configuración correcta con variables de entorno
- ✅ Manejo de errores y fallbacks
- ✅ Análisis comparativo documentado
- ✅ Código limpio y comentado

---

### Ejercicio 2: Optimización de Parámetros
**Objetivo**: Experimentar con parámetros para diferentes casos de uso

**Tareas**:
1. Diseña 5 casos de uso diferentes (creativo, analítico, técnico, etc.)
2. Optimiza temperature, max_tokens, y otros parámetros para cada caso
3. Implementa un sistema de configuraciones predefinidas
4. Mide y compara resultados

**Entregable**: Biblioteca de configuraciones optimizadas con documentación

**Criterios de Evaluación**:
- ✅ Casos de uso bien definidos y justificados
- ✅ Experimentación sistemática con parámetros
- ✅ Medición de resultados (calidad, tiempo, tokens)
- ✅ Documentación de mejores prácticas

---

## 🔧 Ejercicios Intermedios (En Parejas)

### Ejercicio 3: Chatbot Especializado con Streaming
**Objetivo**: Integrar LangChain, streaming y personalización

**Tareas**:
1. Desarrolla un chatbot especializado en un dominio específico
2. Implementa streaming con indicadores visuales
3. Añade comandos especiales (/help, /reset, /config)
4. Incluye sistema de logs y métricas

**Dominios Sugeridos**:
- 🎓 Tutor de programación
- 💼 Asistente de recursos humanos
- 🏥 Asistente médico de información general
- 💰 Consultor financiero básico
- 🎨 Asistente de marketing creativo

**Entregable**: Aplicación funcional con documentación de usuario

**Criterios de Evaluación**:
- ✅ Especialización clara y útil
- ✅ Streaming fluido y responsivo
- ✅ Interfaz de usuario intuitiva
- ✅ Manejo robusto de errores
- ✅ Documentación técnica y de usuario

---

### Ejercicio 4: Sistema de Memoria Inteligente
**Objetivo**: Implementar gestión avanzada de memoria conversacional

**Tareas**:
1. Implementa los 3 tipos de memoria de LangChain
2. Crea un sistema que seleccione automáticamente el tipo de memoria
3. Desarrolla métricas de eficiencia (tokens/costo vs calidad)
4. Implementa persistencia de memoria entre sesiones

**Entregable**: Sistema de memoria adaptativo con análisis de performance

**Criterios de Evaluación**:
- ✅ Implementación correcta de todos los tipos de memoria
- ✅ Lógica inteligente para selección automática
- ✅ Métricas claras y útiles
- ✅ Persistencia funcional
- ✅ Análisis de eficiencia documentado

---

## 🚀 Proyecto Integrador (Evaluación Final)

### Objetivo
Desarrollar una **aplicación completa** que integre todos los conceptos de IL1.1 y sirva como base para el proyecto transversal del curso.

### Casos de Uso Reales para Proyecto Final

Los estudiantes pueden elegir uno de estos casos de uso empresariales reales:

#### 1. 🏢 Sistema de Atención al Cliente Empresarial
**Contexto**: Empresa de software SaaS con 1000+ clientes
**Funcionalidades**:
- Chatbot de primera línea con streaming
- Base de conocimientos integrada
- Escalamiento automático a humanos
- Métricas de satisfacción y resolución

**Tecnologías IL1.1**: API directa + LangChain + Streaming + Memoria resumen
**Complejidad**: Alta
**Aplicación Real**: Zendesk, Intercom, Freshdesk

---

#### 2. 🎓 Asistente de Aprendizaje Personalizado
**Contexto**: Plataforma educativa online con cursos técnicos
**Funcionalidades**:
- Tutor que adapta explicaciones al nivel del estudiante
- Memoria de progreso y preferencias de aprendizaje
- Generación de ejercicios personalizados
- Feedback constructivo automático

**Tecnologías IL1.1**: LangChain + Memoria buffer + Streaming + Configuraciones múltiples
**Complejidad**: Media-Alta
**Aplicación Real**: Khan Academy, Coursera, Duolingo

---

#### 3. 💼 Asistente de Reclutamiento y RRHH
**Contexto**: Consultora de recursos humanos
**Funcionalidades**:
- Screening inicial de candidatos
- Generación de preguntas de entrevista personalizadas
- Análisis de CVs y matching con vacantes
- Asistente para empleados (políticas, beneficios)

**Tecnologías IL1.1**: APIs múltiples + Memoria window + Streaming + Configuraciones especializadas
**Complejidad**: Media
**Aplicación Real**: LinkedIn Talent Hub, BambooHR

---

#### 4. 🏥 Asistente de Información Médica
**Contexto**: Clínica privada con múltiples especialidades
**Funcionalidades**:
- Información general sobre síntomas (sin diagnóstico)
- Preparación para consultas médicas
- Explicación de procedimientos y tratamientos
- Recordatorios y educación preventiva

**Tecnologías IL1.1**: LangChain + Memoria summary + Streaming + Fallbacks seguros
**Complejidad**: Alta (por consideraciones éticas)
**Aplicación Real**: Ada Health, Babylon Health

---

#### 5. 🛒 Asistente de E-commerce Personalizado
**Contexto**: Tienda online de electrónicos
**Funcionalidades**:
- Recomendaciones de productos conversacionales
- Comparación técnica entre productos
- Asistencia post-venta y soporte técnico
- Gestión de devoluciones y garantías

**Tecnologías IL1.1**: API directa + LangChain + Memoria buffer + Streaming
**Complejidad**: Media
**Aplicación Real**: Amazon Alexa Shopping, Shopify Assistant

---

#### 6. 📊 Analista de Datos Conversacional
**Contexto**: Empresa de consultoría de datos
**Funcionalidades**:
- Interpretación de dashboards y métricas
- Generación de insights automáticos
- Explicación de tendencias y anomalías
- Recomendaciones de acción basadas en datos

**Tecnologías IL1.1**: APIs múltiples + Memoria inteligente + Streaming + Configuraciones analíticas
**Complejidad**: Alta
**Aplicación Real**: Tableau Ask Data, Power BI Q&A

---

#### 7. 🏠 Asistente Inmobiliario Virtual
**Contexto**: Agencia inmobiliaria digital
**Funcionalidades**:
- Búsqueda conversacional de propiedades
- Información sobre barrios y servicios
- Cálculo de financiamiento y costos
- Agenda de visitas y seguimiento

**Tecnologías IL1.1**: LangChain + Memoria window + Streaming + Configuraciones especializadas
**Complejidad**: Media
**Aplicación Real**: Zillow, Realtor.com assistants

---

#### 8. 🚗 Asistente de Movilidad Urbana
**Contexto**: Aplicación de transporte multimodal
**Funcionalidades**:
- Planificación de rutas conversacional
- Información en tiempo real de transporte
- Recomendaciones basadas en preferencias
- Asistencia para incidencias y reportes

**Tecnologías IL1.1**: APIs tiempo real + LangChain + Memoria + Streaming
**Complejidad**: Media-Alta
**Aplicación Real**: Google Maps Assistant, Citymapper

---

## 📋 Especificaciones del Proyecto Final

### Requisitos Técnicos Mínimos
1. **Conexión API**: Al menos 1 proveedor configurado correctamente
2. **LangChain**: Uso de al menos 2 componentes del framework
3. **Streaming**: Implementación de respuestas en tiempo real
4. **Memoria**: Gestión de contexto conversacional
5. **Manejo de Errores**: Sistema robusto de error handling
6. **Documentación**: README, configuración y guía de usuario

### Requisitos Funcionales
1. **Interfaz de Usuario**: CLI o web básica pero funcional
2. **Casos de Uso**: Al menos 3 funcionalidades principales
3. **Configuración**: Sistema de configuración flexible
4. **Logs y Métricas**: Monitoreo básico de uso y performance
5. **Testing**: Al menos pruebas básicas de funcionalidad

---

## 📊 Rúbrica de Evaluación

### Implementación Técnica (40%)
| Criterio | Excelente (4) | Bueno (3) | Satisfactorio (2) | Insuficiente (1) |
|----------|---------------|-----------|-------------------|------------------|
| **Configuración API** | Multi-proveedor con fallbacks | Un proveedor robusto | Configuración básica funcional | Configuración incompleta |
| **Uso de LangChain** | Múltiples componentes integrados | 2-3 componentes bien usados | Uso básico correcto | Implementación mínima |
| **Streaming** | Fluido con indicadores visuales | Funcional y responsive | Implementación básica | No funciona correctamente |
| **Memoria** | Sistema inteligente adaptativo | Tipo apropiado bien implementado | Implementación básica | No mantiene contexto |

### Funcionalidad (30%)
| Criterio | Excelente (4) | Bueno (3) | Satisfactorio (2) | Insuficiente (1) |
|----------|---------------|-----------|-------------------|------------------|
| **Casos de Uso** | >3 funcionalidades complejas | 3 funcionalidades completas | 2-3 funcionalidades básicas | <2 funcionalidades |
| **Interfaz Usuario** | Intuitiva y pulida | Funcional y clara | Básica pero usable | Difícil de usar |
| **Manejo Errores** | Robusto y informativo | Adecuado para casos principales | Básico | Mínimo o ausente |

### Documentación (20%)
| Criterio | Excelente (4) | Bueno (3) | Satisfactorio (2) | Insuficiente (1) |
|----------|---------------|-----------|-------------------|------------------|
| **README** | Completo y profesional | Información necesaria clara | Información básica | Incompleto |
| **Código** | Bien comentado y estructurado | Comentarios apropiados | Comentarios básicos | Sin comentarios |
| **Configuración** | Instrucciones detalladas | Pasos claros | Información básica | Incompleto |

### Innovación (10%)
| Criterio | Excelente (4) | Bueno (3) | Satisfactorio (2) | Insuficiente (1) |
|----------|---------------|-----------|-------------------|------------------|
| **Creatividad** | Solución original e innovadora | Implementación creativa | Enfoque estándar | Implementación básica |
| **Valor Agregado** | Funcionalidades únicas | Mejoras significativas | Algunas mejoras | Sin valor agregado |

---

## 📅 Cronograma Sugerido

### Semana 1: Ejercicios Básicos
- **Días 1-2**: Ejercicio 1 (Configuración Multi-Proveedor)
- **Días 3-4**: Ejercicio 2 (Optimización de Parámetros)
- **Día 5**: Revisión y feedback

### Semana 2: Ejercicios Intermedios
- **Días 1-3**: Ejercicio 3 (Chatbot Especializado)
- **Días 4-5**: Ejercicio 4 (Sistema de Memoria)

### Semana 3: Proyecto Final
- **Días 1-2**: Selección de caso de uso y diseño
- **Días 3-4**: Implementación core
- **Día 5**: Testing y documentación

### Semana 4: Presentaciones
- **Días 1-3**: Refinamiento y preparación
- **Días 4-5**: Presentaciones grupales

---

## 💡 Consejos para el Éxito

### Para Estudiantes
1. **Empieza simple**: Implementa funcionalidad básica primero
2. **Itera frecuentemente**: Mejora gradualmente
3. **Documenta todo**: Será útil para el proyecto transversal
4. **Prueba con usuarios reales**: Feedback temprano es valioso
5. **Considera la escalabilidad**: Piensa en el crecimiento futuro

### Para Instructores
1. **Feedback continuo**: Revisiones semanales
2. **Mentoría técnica**: Apoyo en decisiones arquitectónicas
3. **Conexión con industria**: Invita speakers del sector
4. **Evaluación formativa**: Checkpoints regulares
5. **Celebra logros**: Reconoce el progreso incremental

---

## 🔗 Recursos Adicionales

### Documentación Técnica
- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [LangChain Production Guide](https://python.langchain.com/docs/guides/production)
- [GitHub Models Documentation](https://docs.github.com/en/github-models)

### Herramientas Recomendadas
- **Development**: VS Code, Jupyter Lab
- **Testing**: pytest, unittest
- **Documentation**: Sphinx, MkDocs
- **Deployment**: Streamlit, Gradio, FastAPI

### Comunidad y Soporte
- Stack Overflow tags: `langchain`, `openai-api`
- GitHub Discussions en repositorios oficiales
- Discord/Slack de comunidades de IA
- Office hours con instructores

---

*Este documento será actualizado basado en feedback de estudiantes y evolución de las tecnologías.*