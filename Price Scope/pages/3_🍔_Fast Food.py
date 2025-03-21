import streamlit as st


if not st.session_state.get("authenticated", False):
    st.warning("Vous devez être connecté pour accéder à cette page.")
    st.stop()

# Contenu de la page Fast Food pour les utilisateurs connectés
st.title("🍔 Fast Food")
st.write("Bienvenue sur la page Fast Food.")