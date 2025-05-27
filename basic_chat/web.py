import streamlit as st
import requests

st.title('Chat personal con Ollama')

# Entrada de texto para el usuario
user_input = st.text_input("Escribe tu mensaje:", "")

# Botón para enviar el mensaje
if st.button('Enviar'):
    if user_input:
        # Enviar el mensaje al servidor Flask
        response = requests.post('http://127.0.0.1:5050/chat', json={'message': user_input})
        if response.status_code == 200:
            # Mostrar la respuesta en la interfaz
            st.text_area('Respuesta:', value=response.text, height=300)
        else:
            st.error('Error en la respuesta del servidor')
    else:
        st.error('Por favor, escribe un mensaje antes de enviar.')