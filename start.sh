#!/bin/bash

# Colores para mensajes en terminal
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

# Mostrar ayuda si se solicita
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "${GREEN}=== Script de inicio para Chat con Ollama ===${NC}"
    echo "Uso: ./start.sh [tipo_de_agente]"
    echo ""
    echo "Opciones disponibles:"
    echo "  basic_chat       - Inicia el chat básico (por defecto)"
    echo "  agent_with_memory - Inicia el sistema de agentes con memoria"
    echo "  --help, -h       - Muestra este mensaje de ayuda"
    exit 0
fi

# Determinar qué agente iniciar (por defecto: basic_chat)
AGENT_TYPE=${1:-basic_chat}

if [ "$AGENT_TYPE" = "basic_chat" ]; then
    APP_DIR="basic_chat"
    APP_NAME="Chat Personal con Ollama"
elif [ "$AGENT_TYPE" = "agent_with_memory" ]; then
    APP_DIR="agent_with_memory"
    APP_NAME="Sistema de Agentes IA Avanzado"
elif [ "$AGENT_TYPE" = "single_agent" ]; then
    APP_DIR="single_agent"
    APP_NAME="Sistema de Agentes IA"
else
    echo "${YELLOW}Tipo de agente no válido. Opciones: basic_chat, agent_with_memory${NC}"
    echo "Usa './start.sh --help' para más información."
    exit 1
fi

echo "${GREEN}=== Iniciando $APP_NAME ===${NC}"

# Verificar si Ollama está instalado
if ! command -v ollama &> /dev/null; then
    echo "${YELLOW}Ollama no está instalado. Por favor, instálalo primero.${NC}"
    echo "Visita: https://ollama.com para descargar e instalar Ollama."
    exit 1
fi

# Verificar si el modelo llama3.2:1b está instalado
if ! ollama list | grep -q "llama3.2:1b"; then
    echo "${YELLOW}El modelo llama3.2:1b no está instalado. Instalándolo ahora...${NC}"
    ollama pull llama3.2:1b
fi

# Verificar dependencias de Python
echo "${BLUE}Verificando dependencias de Python...${NC}"
pip install -q ollama flask streamlit requests

# Iniciar el servidor Flask en segundo plano
echo "${GREEN}Iniciando servidor Flask...${NC}"
(cd "$APP_DIR" && export FLASK_APP=app.py && export FLASK_ENV=production && exec flask run --port=5050) &
FLASK_PID=$!

# Esperar a que el servidor Flask esté listo
echo "${BLUE}Esperando a que el servidor Flask esté listo...${NC}"
sleep 3

# Iniciar la aplicación Streamlit
echo "${GREEN}Iniciando interfaz web con Streamlit...${NC}"
streamlit run "$APP_DIR/web.py" &
STREAMLIT_PID=$!

# Función para manejar la terminación del script
cleanup() {
    echo "\n${YELLOW}Deteniendo servicios...${NC}"
    kill $FLASK_PID 2>/dev/null
    kill $STREAMLIT_PID 2>/dev/null
    echo "${GREEN}Servicios detenidos. ¡Hasta pronto!${NC}"
    exit 0
}

# Capturar señales de terminación
trap cleanup SIGINT SIGTERM

echo "\n${GREEN}¡Todo listo! La aplicación está ejecutándose.${NC}"
echo "${BLUE}Interfaz web disponible en: ${NC}http://localhost:8501"
echo "${YELLOW}Presiona Ctrl+C para detener todos los servicios.${NC}"

# Mantener el script en ejecución
while true; do
    sleep 1
done