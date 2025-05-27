🤖 TechBot - Chat Interactivo con Ollama y Llama 3.2
📋 Descripción del Proyecto
Este proyecto implementa un chat interactivo con memoria utilizando Ollama y el modelo Llama 3.2. Incluye un agente personalizado (TechBot) especializado en soporte técnico con capacidad de mantener contexto a lo largo de conversaciones completas.
✨ Características Implementadas
🧠 Memoria de Conversación

Persistencia de contexto: El chat mantiene historial completo de la conversación
Memoria dinámica: Cada sesión mantiene su propio contexto independiente
Gestión inteligente: Limita automáticamente el historial para optimizar rendimiento

🤖 Agente Personalizado - TechBot

Personalidad definida: Asistente de soporte técnico amigable y profesional
Especialización: Enfocado en programación y tecnología
Comportamiento consistente: Mantiene su rol a lo largo de toda la conversación
Respuestas estructuradas: Explica conceptos paso a paso con ejemplos prácticos

🖥️ Interfaz de Usuario

Frontend Streamlit: Interfaz web moderna y reactiva
Backend Flask: API REST robusta para gestión de conversaciones
Gestión de sesiones: Múltiples conversaciones independientes
Indicadores visuales: Estados de conexión y contadores de mensajes

🏗️ Arquitectura del Sistema
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐    Python SDK    ┌─────────────────┐
│                 │ ──────────────> │                 │ ───────────────> │                 │
│   Streamlit     │                 │   Flask API     │                  │     Ollama      │
│   (Frontend)    │ <────────────── │   (Backend)     │ <─────────────── │   (Llama 3.2)   │
│                 │    Responses    │                 │    Responses     │                 │
└─────────────────┘                 └─────────────────┘                  └─────────────────┘
Flujo de Datos:

Usuario envía mensaje en Streamlit
Streamlit hace POST a Flask API
Flask recupera historial de conversación (memoria)
Flask envía contexto completo a Ollama
Ollama procesa con Llama 3.2 y responde
Flask guarda respuesta en memoria y la retorna
Streamlit muestra respuesta al usuario

📁 Estructura del Proyecto
proyecto/
├── app.py                 # Servidor Flask con memoria y agente
├── streamlit_app.py       # Interfaz Streamlit
├── test_memory.py         # Script de pruebas automatizadas
├── requirements.txt       # Dependencias Python
└── README.md             # Documentación
🚀 Instalación y Ejecución
Prerequisitos

Ollama instalado: Descargar de ollama.com
Modelo Llama 3.2: ollama pull llama3.2:1b
Python 3.8+

Pasos de instalación:
bash# 1. Clonar o descargar los archivos del proyecto
cd tu-directorio-proyecto

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Verificar que Ollama esté corriendo
ollama list  # Debe mostrar llama3.2:1b

# 4. Ejecutar servidor Flask (Terminal 1)
python app.py

# 5. Ejecutar Streamlit (Terminal 2)
streamlit run streamlit_app.py

# 6. (Opcional) Ejecutar pruebas automatizadas (Terminal 3)
python test_memory.py
URLs de acceso:

Chat Interface: http://localhost:8501
Flask API: http://127.0.0.1:5000
API Endpoints:

POST /chat - Enviar mensaje
POST /reset - Reiniciar conversación
GET /history - Obtener historial



🧪 Pruebas de Funcionalidad
Pruebas Manuales

Memoria: Haz preguntas de seguimiento que dependan de respuestas anteriores
Agente: Observa la personalidad consistente de TechBot
Contexto: Verifica que recuerda información de mensajes previos

Pruebas Automatizadas
Ejecuta python test_memory.py para probar:

✅ Persistencia de memoria
✅ Personalidad del agente
✅ Contexto de conversación
✅ Conectividad con Ollama

Ejemplo de Conversación con Memoria:
Usuario: "Hola, necesito ayuda con Python"
TechBot: "¡Hola! Soy TechBot... ¿Qué aspecto específico de Python te gustaría aprender?"

Usuario: "¿Qué son las listas?"
TechBot: "Las listas en Python son estructuras de datos... [explicación detallada]"

Usuario: "¿Puedes darme un ejemplo de lo que acabas de explicar?"
TechBot: "¡Por supuesto! Basándome en la explicación sobre listas que te di..."
                    ↑ (Demuestra memoria del contexto anterior)
🔧 Configuración del Agente
Personalidad Actual (TechBot):

Rol: Asistente de Soporte Técnico
Especialización: Programación y tecnología
Tono: Amigable, profesional, paciente
Estilo: Explicaciones paso a paso con ejemplos

Personalización:
Para cambiar la personalidad del agente, modifica AGENT_SYSTEM_MESSAGE en app.py:
pythonAGENT_SYSTEM_MESSAGE = {
    'role': 'system',
    'content': 'Tu nueva personalidad aquí...'
}
🎯 Cumplimiento de Requisitos
✅ Requisitos Cumplidos:

Chat interactivo con Ollama y Llama 3.2 ✅

Implementado con Flask + Streamlit
Usa modelo llama3.2:1b


Memoria para mantener contexto ✅

Sistema de historial persistente
Contexto completo en cada llamada
Gestión inteligente de memoria


Agente personalizado ✅

TechBot con personalidad definida
Comportamiento consistente
Especialización en soporte técnico


Investigación de documentación ✅

Implementación basada en mejores prácticas de Ollama
Uso correcto de mensajes con roles (system, user, assistant)


Scripts Python funcionales ✅

Backend Flask robusto
Frontend Streamlit interactivo
Script de pruebas automatizadas



📊 Métricas de Rendimiento

Tiempo de respuesta: ~2-5 segundos (depende del hardware)
Gestión de memoria: Limitado a últimos 20 mensajes + contexto de sistema
Sesiones concurrentes: Soporta múltiples usuarios independientes
Tamaño de contexto: Optimizado para evitar límites de tokens

🔍 Troubleshooting
Problemas Comunes:

"model not found"
bashollama pull llama3.2:1b

"Connection refused"

Verificar que Ollama esté corriendo
Verificar que Flask esté en puerto 5000


Respuestas lentas

Normal con modelos locales
Considera usar modelo más pequeño



🎓 Conceptos Técnicos Implementados
Memoria de Conversación:

Persistencia: Almacenamiento en memoria del servidor
Contexto completo: Cada llamada incluye historial completo
Gestión de tokens: Limita historial para evitar overflow

Agente con Personalidad:

System Message: Define comportamiento del agente
Consistencia: Mantiene personalidad a lo largo de conversación
Especialización: Enfoque específico en soporte técnico

Arquitectura:

Separación de responsabilidades: Frontend/Backend separados
API RESTful: Endpoints bien definidos
Gestión de estado: Sesiones independientes por usuario

🏆 Conclusión
Este proyecto demuestra una implementación completa de un chat inteligente con:

✅ Memoria funcional que mantiene contexto
✅ Agente personalizado con comportamiento consistente
✅ Interfaz profesional fácil de usar
✅ Arquitectura escalable y bien estructurada
✅ Pruebas automatizadas para validar funcionalidad

Todas las especificaciones de la tarea han sido implementadas exitosamente.