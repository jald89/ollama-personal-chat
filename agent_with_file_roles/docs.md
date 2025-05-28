# Sistema de Agentes IA con Roles Personalizables (Flask + Streamlit)

Este sistema permite crear, gestionar y utilizar agentes conversacionales IA con roles personalizados, definidos exclusivamente mediante archivos `.json` en la carpeta `roles/`. Incluye backend en Flask y frontend en Streamlit.

## Estructura de Carpetas

```
agent_with_file_roles/
├── app.py           # Backend Flask
├── web.py           # Frontend Streamlit
├── roles/           # Carpeta de roles (solo .json)
│   ├── techbot.json
│   ├── aitutor.json
│   └── ...
├── docs.md          # (Este archivo)
├── README.md
└── requirements.txt
```

## ¿Cómo funciona?

- **Roles de agentes**: Cada agente se define en un archivo `.json` dentro de `roles/`.
- **Campos requeridos en cada archivo `.json`**:
  - `name`: Nombre del agente.
  - `description`: Descripción breve.
  - `system_message`: Instrucciones de sistema para el agente.
  - `tips`: Consejos o tip personalizado (opcional, pero recomendado).
- **No se aceptan archivos `.txt`**. Solo `.json`.

### Ejemplo de archivo de rol (`roles/aitutor.json`):

```json
{
  "name": "AI Tutor",
  "description": "Un tutor experto en IA generativa y Python.",
  "system_message": "Eres un tutor paciente y claro. Explica conceptos de IA y Python de forma sencilla y con ejemplos prácticos.",
  "tips": "Haz preguntas para guiar el aprendizaje y sugiere recursos adicionales."
}
```

## Backend (Flask)

- **Carga automática** de todos los `.json` en `roles/` al iniciar.
- **Endpoint `/agents`**: Devuelve todos los agentes con `name`, `description` y `tips`.
- **Endpoint `/set_agent`**: Cambia el agente activo para la sesión.
- **Endpoint `/create_custom_agent_from_file`**: Permite crear un agente personalizado desde un archivo `.json` y devuelve también el campo `tips`.
- **Endpoint `/chat`**: Envía mensajes y recibe respuestas del agente seleccionado.
- **Endpoint `/reset`**: Reinicia la conversación de la sesión.

## Frontend (Streamlit)

- Muestra la lista de agentes disponibles y permite seleccionar uno.
- Muestra dinámicamente el tip (`tips`) del agente seleccionado.
- Si el agente no tiene tip, muestra un mensaje por defecto motivador e inspirador.
- Permite crear agentes personalizados desde archivos `.json`.
- Sincroniza y advierte si hay desincronización entre backend y frontend.

## Personalización y Extensión

- Para agregar un nuevo agente, crea un archivo `.json` en `roles/` siguiendo la estructura indicada.
- Reinicia el backend para que el nuevo agente esté disponible.
- Puedes exportar todos los roles a un solo archivo `all_roles.json` si lo necesitas para otros fines.

## Notas Técnicas

- El sistema ya **no soporta archivos `.txt`** para roles.
- El campo `tips` es opcional pero se recomienda para mejorar la experiencia del usuario.
- El backend y frontend están sincronizados para mostrar siempre la información más actualizada de los agentes.

## Ejecución

1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Inicia el backend:
   ```bash
   python app.py
   ```
3. Inicia el frontend:
   ```bash
   streamlit run web.py
   ```

## Endpoints disponibles

- `GET  /agents` — Listar agentes
- `POST /set_agent` — Cambiar agente
- `POST /create_custom_agent_from_file` — Crear agente personalizado desde archivo
- `POST /chat` — Enviar mensaje
- `POST /reset` — Reiniciar conversación

---

**¡Personaliza, experimenta y potencia tus conversaciones con agentes hechos a tu medida!**
