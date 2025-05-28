# Agentes IA con Roles desde Archivos Externos

> **¿Buscas la documentación técnica y explicación de la lógica? Consulta [`docs.md`](./docs.md)**

Este proyecto implementa un sistema de agentes IA donde los roles e instrucciones de cada agente se cargan dinámicamente desde archivos `.json` ubicados en la carpeta `roles/`.

## Características
- Los agentes predefinidos se generan leyendo los archivos `.json` en `roles/`.
- Puedes crear agentes personalizados desde la interfaz web, seleccionando cualquier archivo de rol `.json`.
- El backend y frontend funcionan igual que en `agent_with_memory`, pero la definición de agentes es 100% externa.

## Estructura
```
agent_with_file_roles/
├── app.py
├── web.py
├── requirements.txt
└── roles/
    ├── techbot.json
    ├── mathtutor.json
    ├── chef.json
    ├── fitness.json
    ├── creative.json
    ├── business.json
    ├── aitutor.json
    └── aiprogramer.json
```

## Ejemplo: Crear un nuevo rol (AITutor)

1. Crea un archivo llamado `aitutor.json` en la carpeta `roles/` con el siguiente contenido:

```json
{
  "name": "AITutor",
  "description": "Experto programador en Python y especialista en IA generativa",
  "system_message": "Eres AITutor, un experto programador en Python y especialista en inteligencia artificial generativa. Explicas conceptos avanzados de IA de manera clara y didáctica. Proporcionas ejemplos prácticos en Python. Ayudas a resolver dudas sobre modelos generativos, redes neuronales, y aplicaciones de IA. Motivas a los estudiantes a experimentar y aprender de forma práctica. Mantienes un tono profesional, paciente y entusiasta por la innovación."
}
```

2. Reinicia el backend si ya estaba corriendo.
3. El nuevo agente aparecerá automáticamente en la interfaz web y estará disponible para selección.

## Uso
1. Agrega o edita archivos `.json` en la carpeta `roles/` para definir nuevos agentes.
2. Inicia el backend:
   ```bash
   python app.py
   ```
3. Inicia el frontend:
   ```bash
   streamlit run web.py
   ```
4. Usa la interfaz para seleccionar agentes o crear nuevos desde archivos.

## Endpoints principales
- `GET /agents` — Lista los agentes disponibles (según archivos en `roles/`)
- `POST /set_agent` — Cambia el agente de la sesión
- `POST /create_custom_agent_from_file` — Crea un agente personalizado desde archivo
- `POST /chat` — Envía mensaje y obtiene respuesta
- `POST /reset` — Reinicia la conversación

## Personalización
- Solo necesitas agregar un archivo `.json` en `roles/` para definir un nuevo agente.
- El nombre del archivo será el `agent_id`.
