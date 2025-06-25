# Evaluación IL1.1 - Introducción a LLMs y Conexiones API

## Quiz Formativo (8 preguntas)

### Pregunta 1: Fundamentos de LLMs
**¿Cuál es la arquitectura base de los modelos de lenguaje grandes modernos?**

a) Redes Neuronales Recurrentes (RNN)
b) Redes Neuronales Convolucionales (CNN)
c) Transformers
d) Máquinas de Vector de Soporte (SVM)

**Respuesta correcta: c) Transformers**
*Explicación: Los LLMs modernos como GPT, BERT, y otros están basados en la arquitectura Transformer, que utiliza mecanismos de atención para procesar secuencias de texto.*

---

### Pregunta 2: Tokens y Procesamiento
**¿Qué son los tokens en el contexto de los LLMs?**

a) Claves de autenticación para las APIs
b) Unidades básicas de texto procesadas por el modelo
c) Parámetros de configuración del modelo
d) Variables de entorno del sistema

**Respuesta correcta: b) Unidades básicas de texto procesadas por el modelo**
*Explicación: Los tokens son las unidades básicas en las que se divide el texto para ser procesado por el modelo. Pueden ser palabras, subpalabras, o caracteres dependiendo del tokenizador.*

---

### Pregunta 3: Parámetros de API
**¿Qué efecto tiene aumentar el parámetro "temperature" en una llamada a la API?**

a) Reduce el tiempo de respuesta
b) Aumenta la creatividad y variabilidad de las respuestas
c) Mejora la precisión factual
d) Disminuye el consumo de tokens

**Respuesta correcta: b) Aumenta la creatividad y variabilidad de las respuestas**
*Explicación: Temperature controla la aleatoriedad en la generación. Valores altos (0.7-1.0) producen respuestas más creativas y variables, mientras que valores bajos (0-0.3) producen respuestas más determinísticas.*

---

### Pregunta 4: Configuración de APIs
**¿Cuál es la práctica de seguridad recomendada para manejar API keys?**

a) Incluirlas directamente en el código fuente
b) Guardarlas en variables de entorno
c) Compartirlas en repositorios públicos
d) Codificarlas en base64 en el código

**Respuesta correcta: b) Guardarlas en variables de entorno**
*Explicación: Las API keys deben mantenerse seguras usando variables de entorno, archivos de configuración no versionados, o servicios de gestión de secretos.*

---

### Pregunta 5: LangChain Framework
**¿Cuál es una ventaja principal de usar LangChain en lugar de APIs directas?**

a) Mayor velocidad de respuesta
b) Menor costo por llamada
c) Abstracción y compatibilidad entre proveedores
d) Acceso a modelos exclusivos

**Respuesta correcta: c) Abstracción y compatibilidad entre proveedores**
*Explicación: LangChain proporciona una interfaz unificada que permite cambiar entre diferentes proveedores de LLMs sin modificar el código de aplicación.*

---

### Pregunta 6: Streaming de Respuestas
**¿En qué escenarios es más útil implementar streaming de respuestas?**

a) Cuando se necesita la respuesta completa antes de procesarla
b) Para aplicaciones donde la experiencia de usuario en tiempo real es importante
c) Únicamente para modelos de código abierto
d) Solo cuando se procesan archivos grandes

**Respuesta correcta: b) Para aplicaciones donde la experiencia de usuario en tiempo real es importante**
*Explicación: El streaming permite mostrar la respuesta conforme se genera, mejorando la percepción de velocidad y la experiencia interactiva del usuario.*

---

### Pregunta 7: Gestión de Memoria
**¿Qué tipo de memoria implementa ConversationBufferMemory en LangChain?**

a) Memoria persistente en base de datos
b) Memoria de corto plazo que mantiene todo el historial
c) Memoria que solo guarda la última interacción
d) Memoria distribuida en múltiples servidores

**Respuesta correcta: b) Memoria de corto plazo que mantiene todo el historial**
*Explicación: ConversationBufferMemory mantiene todo el historial de la conversación en memoria, lo que puede consumir muchos tokens en conversaciones largas.*

---

### Pregunta 8: Mejores Prácticas
**¿Cuál de las siguientes NO es una buena práctica al trabajar con LLMs?**

a) Implementar manejo de errores y reintentos
b) Validar y sanitizar las entradas del usuario
c) Asumir que todas las respuestas son factualmente correctas
d) Configurar límites de tiempo (timeouts) apropiados

**Respuesta correcta: c) Asumir que todas las respuestas son factualmente correctas**
*Explicación: Los LLMs pueden generar información incorrecta o "alucinar". Siempre se debe verificar información crítica y no asumir que las respuestas son 100% precisas.*

---

## Evaluación Práctica

### Ejercicio 1: Configuración de API (25 puntos)
Configura una conexión API usando tanto el cliente directo de OpenAI como LangChain. Demuestra:
- Configuración correcta de variables de entorno
- Manejo de errores básico
- Comparación de respuestas entre ambos métodos

### Ejercicio 2: Implementación de Streaming (25 puntos)
Implementa una función que:
- Reciba un prompt del usuario
- Use streaming para mostrar la respuesta en tiempo real
- Maneje correctamente la concatenación de chunks
- Incluya indicadores de progreso

### Ejercicio 3: Sistema de Memoria (25 puntos)
Crea un chatbot simple que:
- Mantenga el contexto de la conversación
- Permita al usuario hacer referencias a mensajes anteriores
- Implemente límites de memoria para evitar exceso de tokens
- Proporcione un comando para limpiar el historial

### Ejercicio 4: Prompt Engineering (25 puntos)
Diseña y prueba prompts para:
- Un asistente de código que explique funciones
- Un analizador de sentimientos con ejemplos
- Un generador de contenido con formato específico
- Documenta el proceso de iteración y mejora

---

## Criterios de Evaluación

### Conocimiento Teórico (40%)
- Comprensión de conceptos fundamentales de LLMs
- Conocimiento de arquitecturas y proveedores
- Entendimiento de parámetros y configuraciones

### Implementación Práctica (40%)
- Código funcional y bien estructurado
- Manejo apropiado de errores
- Seguimiento de mejores prácticas de seguridad
- Calidad de la documentación del código

### Análisis y Reflexión (20%)
- Capacidad de comparar diferentes enfoques
- Identificación de ventajas y limitaciones
- Propuestas de mejoras y optimizaciones
- Consideraciones éticas y de seguridad

---

## Recursos de Apoyo

### Documentación Técnica
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [LangChain Python Docs](https://python.langchain.com/docs/)
- [GitHub Models Guide](https://docs.github.com/en/github-models)

### Herramientas de Desarrollo
- Jupyter Notebooks para prototipado
- VS Code con extensiones de Python
- Postman para pruebas de API
- Git para control de versiones

### Comunidad y Soporte
- Stack Overflow para resolución de problemas
- GitHub Discussions en repositorios oficiales
- Discord/Slack de comunidades de IA
- Documentación oficial de cada proveedor

---

## Entregables

1. **Notebooks completados** con implementaciones funcionales
2. **Documento de análisis** (500-750 palabras) comparando enfoques
3. **Código fuente** con comentarios y documentación
4. **Presentación** (5-7 minutos) demostrando los ejercicios

### Formato de Entrega
- Repositorio GitHub con estructura organizada
- README.md con instrucciones de ejecución
- Requirements.txt con dependencias
- .env.example con variables de entorno requeridas

### Fechas Importantes
- **Entrega parcial**: Ejercicios 1 y 2 completados
- **Entrega final**: Todos los ejercicios y documentación
- **Presentaciones**: Sesión grupal de demostraciones