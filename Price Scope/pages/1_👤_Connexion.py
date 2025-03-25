import streamlit as st
import hashlib
import mysql.connector
from connexion import connect_to_db

# Fonction pour hasher les mots de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fonction pour vérifier les identifiants
def check_credentials(username, password):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hash_password(password)))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user
    return None

# Fonction pour inscrire un nouvel utilisateur
def register_user(username, password, email):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, 'utilisateur')", (username, hash_password(password), email))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    return False

# Vérifier l'état de session
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "role" not in st.session_state:
    st.session_state["role"] = ""
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

# Page de connexion
if not st.session_state["authenticated"]:
    st.title("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        user = check_credentials(username, password)
        if user:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = user['role']
            st.session_state["user_id"] = user['id']
            st.success("Connexion réussie !")
        else:
            st.error("Identifiants incorrects.")

    st.write("Pas encore inscrit ?")
    if st.button("S'inscrire"):
        st.session_state["show_registration"] = True

    if st.session_state.get("show_registration", False):
        st.title("Inscription")
        new_username = st.text_input("Nom d'utilisateur", key="new_username")
        new_password = st.text_input("Mot de passe", type="password", key="new_password")
        email = st.text_input("Email")

        if st.button("S'inscrire", key="register"):
            if register_user(new_username, new_password, email):
                st.success("Inscription réussie ! Vous pouvez maintenant vous connecter.")
                st.session_state["show_registration"] = False
            else:
                st.error("Erreur lors de l'inscription. Veuillez réessayer.")
else:
    st.sidebar.success(f"Connecté en tant que : {st.session_state['username']} ({st.session_state['role']})")
    # Pages restreintes accessibles uniquement après authentification
    st.title("Vous êtes connecté !")
    st.write("Vous pouvez naviguer librement dans l'application.")
    st.write("Pour vous déconnecter, cliquez sur le bouton 'Se déconnecter' dans la barre latérale.")
if st.sidebar.button("Se déconnecter"):
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""
    st.session_state["user_id"] = None
    st.experimental_rerun()