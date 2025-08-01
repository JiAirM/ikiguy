# Save this code as app_ikiguy.py

import streamlit as st
import os
from dotenv import load_dotenv
from mistralai.client import MistralClient # Assuming you have the Mistral AI library installed

# Load API key
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY") # Using MISTRAL_API_KEY

if not mistral_api_key:
    st.error("Mistral API key not found. Please set the MISTRAL_API_KEY environment variable or create a .env file.")
else:
    # Configure Mistral AI client
    client = MistralClient(api_key=mistral_api_key)

    def generate_ikiguy_response(user_input):
        """Generates a response from the Ikiguy chatbot based on user input using Mistral AI."""
        # You may need to adjust the model name based on the Mistral AI models available
        model_name = "mistral-tiny" # Example model name

        messages = [
            {"role": "system", "content": """
             Tu t'appelles Ikiguy.
             Tu es un conseiller d'orientation dans le cadre d'un forum éducatif.
             Tes réponses doivent être simple et faire maximum 2 phrases. 
             Tu dois tutoyer ton interlocuteur.
             Recadre la conversation si l'étudiant ne te parle pas de son orientation.
             Si l'étudiant sait ce qu'il veut faire, conseille le sur le meilleur parcours ou moyens d'exercer son métier.
             Si l'étudiant ne sait pas ce qu'il veut faire, inspire toi des principes de l'Ikigai pour l'orienter vers des choix qui le passionnent, qui sont en demande sur le marché du travail, et qui correspondent à aux compétences de l'étudiant.
             """},
            {"role": "user", "content": user_input}
        ]

        try:
            chat_response = client.chat(
                model=model_name,
                messages=messages
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            return f"Désolé, j'ai rencontré un problème pour générer une réponse avec Mistral AI. Erreur: {e}"


    # Streamlit Interface
    st.set_page_config(layout="wide") # Use wide layout

    # Create columns for layout
    col1, col2, col3 = st.columns([1, 2, 1]) # Adjust column ratios as needed

    with col1:
        st.image("images/Logo BUGA Blob.png", width=150) # Logo in column 1

    with col2:
        st.title("Ikiguy - Ton conseiller d'orientation")

    with col3:
         st.image("images/iki new.png", width=150) # Second image in column 3


    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input field for user query
    user_input = st.chat_input("Avec quoi puis-je t'aider ?")

    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get and display Ikiguy's response
        with st.chat_message("assistant"):
            response = generate_ikiguy_response(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.markdown(response)