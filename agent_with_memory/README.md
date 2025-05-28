# Sistema de Agentes IA con Memoria

> **¿Buscas la documentación técnica y explicación de la lógica? Consulta [`docs.md`](./docs.md)**

## 📋 Descripción del Proyecto

Este proyecto implementa un chat interactivo con memoria utilizando Ollama y el modelo Llama 3.2. Incluye múltiples agentes personalizados con diferentes personalidades y especialidades, todos con capacidad de mantener contexto a lo largo de conversaciones completas.
## ✨ Características Implementadas

### 🧠 Memoria de Conversación

- **Persistencia de contexto**: El chat mantiene historial completo de la conversación
- **Memoria dinámica**: Cada sesión mantiene su propio contexto independiente
- **Gestión inteligente**: Limita automáticamente el historial para optimizar rendimiento

### 🤖 Múltiples Agentes Personalizados

- **TechBot** (Soporte Técnico): Especializado en programación y tecnología
- **MathBot** (Tutor de Matemáticas): Explica conceptos matemáticos paso a paso
- **ChefBot** (Chef Personal): Experto en cocina internacional y recetas
- **FitBot** (Entrenador Personal): Especializado en fitness y nutrición
- **CreativeBot** (Asistente Creativo): Ayuda con proyectos artísticos y creativos
- **BizBot** (Consultor de Negocios): Orientado a estrategias empresariales

Cada agente tiene:
- **Personalidad definida**: Comportamiento y tono consistentes
- **Especialización temática**: Conocimientos enfocados en su área
- **Comportamiento consistente**: Mantiene su rol a lo largo de toda la conversación
- **Respuestas estructuradas**: Explica conceptos de forma clara y organizada

### 🖥️ Interfaz de Usuario

- **Frontend Streamlit**: Interfaz web moderna y reactiva
- **Backend Flask**: API REST robusta para gestión de conversaciones
- **Gestión de sesiones**: Múltiples conversaciones independientes
- **Indicadores visuales**: Estados de conexión y contadores de mensajes
- **Creación de agentes personalizados**: Interfaz para definir nuevos agentes

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐    Python SDK    ┌─────────────────┐
│                 │ ──────────────> │                 │ ───────────────> │                 │
│   Streamlit     │                 │   Flask API     │                  │     Ollama      │
│   (Frontend)    │ <────────────── │   (Backend)     │ <─────────────── │   (Llama 3.2)   │
│                 │    Responses    │                 │    Responses     │                 │
└─────────────────┘                 └─────────────────┘                  └─────────────────┘
```

### Flujo de Datos:

1. Usuario envía mensaje en Streamlit
2. Streamlit hace POST a Flask API
3. Flask recupera historial de conversación (memoria)
4. Flask envía contexto completo a Ollama
5. Ollama procesa con Llama 3.2 y responde
6. Flask guarda respuesta en memoria y la retorna
7. Streamlit muestra respuesta al usuario

## 📁 Estructura del Proyecto

```
agent_with_memory/
├── app.py                 # Servidor Flask con memoria y agentes
├── web.py                 # Interfaz Streamlit
├── test_memory.py         # Script de pruebas automatizadas
├── requirements.txt       # Dependencias Python
└── README.md              # Documentación
```
## 🚀 Instalación y Ejecución

### Prerequisitos

- Ollama instalado: Descargar de [ollama.com](https://ollama.com)
- Modelo Llama 3.2: `ollama pull llama3.2:1b`
- Python 3.8+

### Pasos de instalación:

```bash
# 1. Clonar o descargar los archivos del proyecto
cd tu-directorio-proyecto

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Verificar que Ollama esté corriendo
ollama list  # Debe mostrar llama3.2:1b
```

### Opción 1: Inicio Rápido (Recomendado)

```bash
# Desde la carpeta raíz del proyecto
./start.sh agent_with_memory
```

> **Nota:** El comando `npm run start-agent` solo funciona si tienes el script definido en el `package.json` de la raíz del monorepo. Si no usas Node.js, ejecuta el script bash directamente como arriba.

### Opción 2: Inicio Manual

```bash
# Terminal 1 - Ejecutar servidor Flask
python app.py
# o
flask run --port=5050
 
# Terminal 2 - Ejecutar Streamlit
streamlit run web.py

# Terminal 3 (Opcional) - Ejecutar pruebas automatizadas
python test_memory.py
```

### URLs de acceso:

- **Chat Interface**: http://localhost:8501
- **Flask API**: http://127.0.0.1:5050

### API Endpoints:

- **GET /agents** - Listar agentes disponibles
- **POST /set_agent** - Cambiar agente
- **POST /create_custom_agent** - Crear agente personalizado
- **POST /chat** - Enviar mensaje
- **POST /reset** - Reiniciar conversación



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

## 💬 Ejemplos de Uso por Agente

### TechBot (Soporte Técnico)
- "¿Cómo instalo Python en Windows?"
- "Explícame qué son las APIs REST"
- "Tengo un error en mi código JavaScript: Uncaught TypeError"

### MathBot (Tutor de Matemáticas)
- "¿Cómo resuelvo ecuaciones cuadráticas?"
- "Explícame el teorema de Pitágoras con ejemplos"
- "Necesito ayuda con cálculo diferencial"

### ChefBot (Chef Personal)
- "Receta para pasta sin gluten"
- "¿Cómo preparar un risotto perfecto?"
- "Ideas para cena romántica vegetariana"

### FitBot (Entrenador Personal)
- "Rutina para principiantes en casa"
- "Ejercicios para mejorar resistencia"
- "Plan de alimentación para ganar músculo"

### CreativeBot (Asistente Creativo)
- "Ideas para un proyecto de fotografía"
- "¿Cómo superar el bloqueo creativo?"
- "Técnicas de pintura para principiantes"

### BizBot (Consultor de Negocios)
- "¿Cómo crear un plan de negocios?"
- "Estrategias de marketing digital"
- "Consejos para una startup tecnológica"

### Ejemplo de Conversación con Memoria:

Usuario: "Hola, necesito ayuda con Python"

TechBot: "¡Hola! Soy TechBot... ¿Qué aspecto específico de Python te gustaría aprender?"

Usuario: "¿Qué son las listas?"

TechBot: "Las listas en Python son estructuras de datos... [explicación detallada]"

Usuario: "¿Puedes darme un ejemplo de lo que acabas de explicar?"

TechBot: "¡Por supuesto! Basándome en la explicación sobre listas que te di..."
                    ↑ (Demuestra memoria del contexto anterior)
## 🔧 Configuración de Agentes

### Agentes Predefinidos

El sistema incluye varios agentes predefinidos con diferentes personalidades:

| Agente | Rol | Especialización | Tono | Estilo |
|--------|-----|----------------|------|--------|
| TechBot | Asistente de Soporte Técnico | Programación y tecnología | Amigable, profesional | Explicaciones paso a paso con ejemplos |
| MathBot | Tutor de Matemáticas | Conceptos matemáticos | Paciente, motivador | Analogías y verificación de comprensión |
| ChefBot | Chef Personal | Cocina internacional | Apasionado, creativo | Recetas adaptables con tips profesionales |
| FitBot | Entrenador Personal | Fitness y nutrición | Motivador, enérgico | Rutinas personalizadas con técnicas correctas |
| CreativeBot | Asistente Creativo | Proyectos artísticos | Inspirador, no crítico | Sugerencias específicas para superar bloqueos |
| BizBot | Consultor de Negocios | Estrategias empresariales | Profesional, orientado a resultados | Análisis de viabilidad y estrategias accionables |

### Personalización de Agentes

Hay dos formas de personalizar los agentes:

#### 1. Desde la Interfaz Web

Utiliza la sección "Crear Agente Personalizado" en el sidebar de la interfaz web para definir:
- Nombre del agente
- Instrucciones y personalidad detalladas

#### 2. Modificando el Código

Para añadir nuevos agentes predefinidos, modifica el diccionario `AVAILABLE_AGENTS` en `app.py`:

```python
AVAILABLE_AGENTS = {
    "nuevo_agente": {
        "name": "Nombre del Agente",
        "description": "Descripción corta",
        "system_message": '''Instrucciones detalladas sobre la personalidad, 
        comportamiento y especialización del agente...'''
    },
    # ... otros agentes existentes
}
## 🎯 Cumplimiento de Requisitos

| Requisito | Estado | Detalles |
|-----------|--------|----------|
| **Chat interactivo con Ollama y Llama 3.2** | ✅ | • Implementado con Flask + Streamlit<br>• Usa modelo llama3.2:1b |
| **Memoria para mantener contexto** | ✅ | • Sistema de historial persistente<br>• Contexto completo en cada llamada<br>• Gestión inteligente de memoria |
| **Múltiples agentes personalizados** | ✅ | • 6 agentes predefinidos con personalidades distintas<br>• Comportamiento consistente<br>• Especialización por áreas temáticas |
| **Investigación de documentación** | ✅ | • Implementación basada en mejores prácticas de Ollama<br>• Uso correcto de mensajes con roles (system, user, assistant) |
| **Scripts Python funcionales** | ✅ | • Backend Flask robusto<br>• Frontend Streamlit interactivo<br>• Script de pruebas automatizadas |

## 📊 Métricas de Rendimiento

| Métrica | Valor | Notas |
|---------|-------|-------|
| **Tiempo de respuesta** | ~2-5 segundos | Depende del hardware |
| **Gestión de memoria** | 20 mensajes + sistema | Optimizado para balance entre contexto y rendimiento |
| **Sesiones concurrentes** | Múltiples | Cada usuario mantiene sesión independiente |
| **Tamaño de contexto** | Optimizado | Evita límites de tokens del modelo |

## 🔍 Solución de Problemas

| Problema | Solución |
|----------|----------|
| **"model not found"** | ```bash
ollama pull llama3.2:1b
``` |
| **"Connection refused"** | • Verificar que Ollama esté corriendo<br>• Verificar que Flask esté en puerto 5050 |
| **Respuestas lentas** | • Normal con modelos locales<br>• Considera usar modelo más pequeño |

## 🎓 Conceptos Técnicos Implementados

### Memoria de Conversación
- **Persistencia**: Almacenamiento en memoria del servidor
- **Contexto completo**: Cada llamada incluye historial completo
- **Gestión de tokens**: Limita historial para evitar overflow

### Agentes con Personalidad
- **System Message**: Define comportamiento del agente
- **Consistencia**: Mantiene personalidad a lo largo de conversación
- **Especialización**: Enfoque específico por área temática

### Arquitectura
- **Separación de responsabilidades**: Frontend/Backend separados
- **API RESTful**: Endpoints bien definidos
- **Gestión de estado**: Sesiones independientes por usuario

## 🏆 Conclusión

Este proyecto demuestra una implementación completa de un sistema de chat inteligente con:

- ✅ **Memoria funcional** que mantiene contexto a lo largo de conversaciones
- ✅ **Múltiples agentes personalizados** con comportamientos consistentes
- ✅ **Interfaz profesional** fácil de usar con opciones de personalización
- ✅ **Arquitectura escalable** y bien estructurada para futuras expansiones
- ✅ **Pruebas automatizadas** para validar la funcionalidad

Todas las especificaciones del proyecto han sido implementadas exitosamente, creando un sistema versátil que puede adaptarse a diferentes necesidades de conversación.