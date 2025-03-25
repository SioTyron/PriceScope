import streamlit as st


if not st.session_state.get("authenticated", False):
    st.warning("Vous devez être connecté pour accéder à cette page.")
    st.stop()

# Contenu de la page Bricolage pour les utilisateurs connectés
st.title("⛽︎ Essence")
st.write("Bienvenue sur la page Essence.")
