#!/bin/bash

# Colores para mensajes en terminal
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

echo "${GREEN}=== Iniciando Chat Personal con Ollama ===${NC}"

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
flask run &
FLASK_PID=$!

# Esperar a que el servidor Flask esté listo
echo "${BLUE}Esperando a que el servidor Flask esté listo...${NC}"
sleep 3

# Iniciar la aplicación Streamlit
echo "${GREEN}Iniciando interfaz web con Streamlit...${NC}"
streamlit run web.py &
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