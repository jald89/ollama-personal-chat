# Chat Personal con Ollama

Este proyecto implementa un chat interactivo utilizando Ollama con el modelo Llama 3.2, ofreciendo dos versiones diferentes:

1. **Chat Básico** - Una interfaz simple para conversar con el modelo.
2. **Sistema de Agentes IA** - Una versión avanzada con múltiples personalidades y memoria persistente.

## Requisitos Previos

- [Ollama](https://ollama.com) instalado
- Modelo llama3.2:1b descargado (`ollama pull llama3.2:1b`)
- Python 3.8 o superior
- Dependencias: Flask, Streamlit, Requests, Ollama

## Instalación

1. Clona o descarga este repositorio
2. Instala las dependencias:
   ```
   pip install -r agent_with_memory/requirements.txt
   ```

## Ejecución del Proyecto

### Opción 1: Inicio Rápido (Recomendado)

Puedes iniciar cualquiera de las dos versiones del chat con un solo comando:

```bash
# Iniciar el chat básico (por defecto)
./start.sh
# o
npm run start-basic

# Iniciar el sistema de agentes con memoria
./start.sh agent_with_memory
# o
npm run start-agent
```

El script verificará automáticamente:
- La instalación de Ollama
- La disponibilidad del modelo llama3.2:1b
- Las dependencias de Python necesarias

Y luego iniciará tanto el servidor Flask como la aplicación Streamlit.

### Opción 2: Inicio Manual

Si prefieres iniciar los componentes por separado:

#### Chat Básico

```bash
# Terminal 1 - Servidor Flask
python basic_chat/app.py
# o
npm run start-flask-basic

# Terminal 2 - Interfaz Streamlit
streamlit run basic_chat/web.py
# o
npm run start-streamlit-basic
```

#### Sistema de Agente de servicio tecnico

```bash
# Terminal 1 - Servidor Flask
python single_agent/app.py
# o
npm run start-flask-agent

# Terminal 2 - Interfaz Streamlit
streamlit run single_agent/web.py
# o
npm run start-single
```

#### Sistema de Agentes

```bash
# Terminal 1 - Servidor Flask
python agent_with_memory/app.py
# o
npm run start-flask-agent

# Terminal 2 - Interfaz Streamlit
streamlit run agent_with_memory/web.py
# o
npm run start-streamlit-agent
```

## Acceso a la Aplicación

- **Interfaz Web**: http://localhost:8501
- **API Flask**: http://127.0.0.1:5050

## Agentes Disponibles

El sistema de agentes con memoria incluye las siguientes personalidades:

- **TechBot** - Asistente de Soporte Técnico especializado en programación y tecnología
- **MathBot** - Tutor de Matemáticas que explica conceptos paso a paso
- **ChefBot** - Chef Personal experto en cocina internacional
- **FitBot** - Entrenador Personal para rutinas y consejos de fitness
- **CreativeBot** - Asistente Creativo para proyectos artísticos
- **BizBot** - Consultor de Negocios para estrategias empresariales

Además, puedes crear agentes personalizados con instrucciones específicas desde la interfaz.

## Ayuda

Para ver todas las opciones disponibles:

```bash
./start.sh --help
```

## Solución de Problemas

- Si encuentras errores de conexión, asegúrate de que Ollama esté en ejecución
- Para problemas con el modelo, verifica que llama3.2:1b esté instalado: `ollama list`
- Si las dependencias fallan, ejecuta manualmente: `pip install ollama flask streamlit requests`