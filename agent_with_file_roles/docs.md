# Documentación Técnica: agent_with_file_roles

## Descripción General

Este sistema implementa agentes IA donde los roles e instrucciones se cargan dinámicamente desde archivos de texto en la carpeta `roles/`. Permite máxima flexibilidad y personalización sin modificar el código fuente.

---

## Arquitectura
- **Backend:** Flask (`app.py`)
- **Frontend:** Streamlit (`web.py`)
- **Roles:** Archivos `.txt` en `roles/` (uno por agente)
- **Modelo LLM:** Ollama con `llama3.2:1b`

---

## Lógica de Carga de Agentes
- Al iniciar, el backend lee todos los archivos `.txt` en `roles/` y crea el diccionario de agentes.
- Cada archivo define el `system_message` de un agente.
- El nombre del archivo (sin extensión) es el `agent_id`.
- Puedes crear agentes personalizados desde la interfaz web, seleccionando cualquier archivo de rol.

---

## Endpoints
- `GET /agents` — Lista los agentes disponibles (según archivos en `roles/`)
- `POST /set_agent` — Cambia el agente de la sesión
- `POST /create_custom_agent_from_file` — Crea un agente personalizado desde archivo
- `POST /chat` — Envía mensaje y obtiene respuesta
- `POST /reset` — Reinicia la conversación

---

## Flujo de Datos
1. El usuario selecciona un agente o crea uno personalizado desde archivo.
2. El frontend envía el mensaje y el `agent_id` al backend.
3. El backend usa el contenido del archivo correspondiente como instrucciones del agente.
4. El historial de la conversación se mantiene por sesión.

---

## Ejemplo de Estructura de roles/
```
roles/
├── techbot.txt
├── mathtutor.txt
├── chef.txt
├── fitness.txt
├── creative.txt
└── business.txt
```

---

## Personalización
- Para agregar un nuevo agente, solo crea un archivo `.txt` en `roles/`.
- El contenido del archivo será el prompt/instrucciones del agente.
