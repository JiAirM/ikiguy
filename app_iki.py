# Save this code as app_ikiguy.py

import streamlit as st
# No need for os and dotenv anymore for the API key
from mistralai.client import MistralClient # Assuming you have the Mistral AI library installed

# Load API key using Streamlit's secrets management
try:
    mistral_api_key = st.secrets["MISTRAL_API_KEY"]
except KeyError:
    st.error("Mistral API key not found in Streamlit secrets. Please add it to your app's secrets in Streamlit Cloud.")
    st.stop() # Stop the app if the key is not found


# Configure Mistral AI client
client = MistralClient(api_key=mistral_api_key)

def generate_ikiguy_response(user_input):
    """Generates a response from the Ikiguy chatbot based on user input using Mistral AI."""
    # You may need to adjust the model name based on the Mistral AI models available
    model_name = "mistral-tiny" # Example model name

    messages = [
        {"role": "system", "content": """Tu es Ikiguy, un conseiller d'orientation pour adolescents lors d'un forum éducatif.
Tes réponses doivent être courtes et en langage simple.
Tu dois tutoyer ton interlocuteur.
Tu dois poser une seule question à la fois.
Si l'adolescent sait ce qu'il veut faire, conseille-le sur le meilleur parcours ou les meilleurs moyens d'exercer ce métier.
S'il ne sait pas ce qu'il ne sait pas quoi faire, inspire-toi des principes de l'Ikigai (ce qu'il aime, ce pour quoi il est doué, ce dont le monde a besoin, ce pour quoi il peut être payé) forcer le a trouver des idées.
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