# Chat Personal con Ollama (Versión Básica)

Este proyecto implementa un chatbot personal que utiliza Ollama con el modelo Llama 3.2 para procesar consultas y generar respuestas. Consta de un backend en Flask y una interfaz de usuario en Streamlit.

Esta es la versión básica del chat, que proporciona una interfaz simple para interactuar con el modelo de lenguaje sin funcionalidades avanzadas como memoria o personalidades.

## Requisitos Previos

### Paso 1: Descarga e Instalación de Ollama

1. Visita el sitio web de Ollama:
   - Abre tu navegador y navega a [ollama.com](https://ollama.com).
   - Busca la sección de descargas y selecciona la versión adecuada para tu sistema operativo (Windows, macOS, etc.).

2. Descarga e Instala:
   - Haz clic en el botón de descarga.
   - Una vez descargado el archivo ejecutable, haz doble clic en él para comenzar la instalación.
   - Sigue las instrucciones en pantalla para completar el proceso.

### Paso 2: Verificación de la Instalación de Ollama

1. Abre la terminal:
   - Para Windows, abre la terminal escribiendo `cmd` en el menú de inicio.
   - Para Mac o Linux, puedes usar la aplicación "Terminal".

2. Comprueba la instalación:
   - En la terminal, escribe el siguiente comando para verificar que Ollama se haya instalado correctamente:
     ```
     ollama -v
     ```
   - Esto debería mostrar la versión instalada de Ollama, confirmando que la instalación fue exitosa.

### Paso 3: Instalación del Modelo Llama 3.2

1. Descarga el Modelo Llama 3.2:
   - Ejecuta el siguiente comando para descargar e instalar el modelo:
     ```
     ollama pull llama3.2:1b
     ```
   - Esto descargará e instalará el modelo en tu máquina.

2. Verifica la Instalación del Modelo:
   - Puedes listar los modelos disponibles en Ollama con:
     ```
     ollama list
     ```
   - Deberías ver llama3.2:1b en la lista de modelos instalados.

## Instalación del Proyecto

### Paso 4: Instalar Dependencias de Python

1. Instala las bibliotecas necesarias:
   ```
   pip install ollama flask streamlit requests
   ```

### Paso 5: Clonar o Descargar este Repositorio

1. Clona este repositorio o descarga los archivos en tu máquina local.

## Ejecución del Proyecto

### Opción 1: Inicio Rápido (Recomendado)

1. Abre una terminal y navega hasta la carpeta del proyecto.
2. Ejecuta el script de inicio:
   ```
   ./start.sh
   ```
   o si tienes Node.js instalado:
   ```
   npm start
   ```
3. El script iniciará automáticamente tanto el servidor Flask como la aplicación Streamlit, y te mostrará las URLs para acceder a la interfaz.
4. Para detener todos los servicios, simplemente presiona Ctrl+C en la terminal donde ejecutaste el script.

### Opción 2: Inicio Manual

#### Paso 1: Iniciar el Servidor Backend

1. Abre una terminal y navega hasta la carpeta del proyecto.
2. Ejecuta el servidor Flask:
   ```
   python app.py
   ```
   o
   ```
   flask run port=5050
   ```
3. El servidor debería iniciarse en http://127.0.0.1:5000

#### Paso 2: Iniciar la Interfaz Web

1. Abre otra terminal y navega hasta la carpeta del proyecto.
2. Ejecuta la aplicación Streamlit:
   ```
   streamlit run web.py
   ```
3. Se abrirá automáticamente una ventana del navegador con la interfaz web, o puedes acceder a ella en http://localhost:8501

## Uso

1. En la interfaz web, escribe tu mensaje en el campo de texto.
2. Haz clic en el botón "Enviar".
3. Espera a que el modelo procese tu consulta y muestre la respuesta.

### Ejemplos de Consultas

Puedes hacer preguntas sobre diversos temas como:

- "¿Qué es la inteligencia artificial?"
- "Explícame cómo funciona un motor de combustión interna"
- "Escribe un poema sobre la naturaleza"
- "¿Cuáles son los principios básicos de la programación?"
- "Dame una receta de pan casero"

Recuerda que este chat básico no mantiene el contexto de la conversación, por lo que cada pregunta es tratada de forma independiente.

## Solución de Problemas

- Si encuentras errores relacionados con la conexión al servidor Flask, asegúrate de que el servidor esté ejecutándose en http://127.0.0.1:5000.
- Si el modelo no responde, verifica que Ollama esté funcionando correctamente y que el modelo llama3.2:1b esté instalado.

## Notas

- Este proyecto utiliza el modelo llama3.2:1b, pero puedes modificar el archivo app.py para usar otros modelos disponibles en Ollama.
- Para una mejor experiencia, se recomienda ejecutar este proyecto en una máquina con suficientes recursos (especialmente RAM).
- Esta versión básica no incluye memoria de conversación. Cada mensaje es procesado de forma independiente.
- Si necesitas funcionalidades avanzadas como memoria persistente o agentes especializados, considera usar la versión "agent_with_memory" del proyecto.
- El puerto predeterminado para el servidor Flask es 5050 y para Streamlit es 8501.