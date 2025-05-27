#!/bin/bash

# Colores para mensajes
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

# Función para matar procesos
kill_process() {
    local name=$1
    local pattern=$2
    
    echo -e "${YELLOW}Buscando procesos de $name...${NC}"
    pids=$(pgrep -f "$pattern")
    
    if [ -n "$pids" ]; then
        echo -e "${RED}Deteniendo $name (PIDs: $pids)...${NC}"
        kill $pids
        echo -e "${GREEN}$name detenido${NC}"
    else
        echo -e "${YELLOW}$name no estaba en ejecución${NC}"
    fi
}

# Detener Flask
kill_process "Flask" "flask run --port=5050"

# Detener Streamlit
kill_process "Streamlit" "streamlit run .*/web.py"

echo -e "\n${GREEN}¡Todos los servicios han sido detenidos!${NC}"