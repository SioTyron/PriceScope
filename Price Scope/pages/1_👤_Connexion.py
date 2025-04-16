import streamlit as st
import hashlib
import mysql.connector
from datetime import datetime, timedelta
from streamlit_cookies_controller import CookieController
from connexion import connect_to_db

# Initialisation du contrôleur de cookies
cookie = CookieController()
COOKIE_EXPIRE_MINUTES = 30

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

# Fonction à utiliser dans toutes les pages pour reconnecter automatiquement via cookie
def check_auto_login():
    session_info = cookie.get("auth")
    if session_info and datetime.fromisoformat(session_info["expires_at"]) > datetime.utcnow():
        st.session_state["authenticated"] = True
        st.session_state["username"] = session_info["username"]
        st.session_state["role"] = session_info["role"]
        st.session_state["user_id"] = session_info["user_id"]
    else:
        st.session_state["authenticated"] = False

# Vérification via cookie si la session est encore valide
check_auto_login()

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
            expires_at = datetime.utcnow() + timedelta(minutes=COOKIE_EXPIRE_MINUTES)
            cookie.set("auth", {
                "username": user['username'],
                "role": user['role'],
                "user_id": user['id'],
                "expires_at": expires_at.isoformat()
            })

            st.session_state["authenticated"] = True
            st.session_state["username"] = user['username']
            st.session_state["role"] = user['role']
            st.session_state["user_id"] = user['id']
            st.success("Connexion réussie !")
            st.rerun()
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
    st.title("Vous êtes connecté !")
    st.write("Pour vous déconnecter, cliquez sur le bouton 'Se déconnecter' dans la barre latérale.")

if st.sidebar.button("Se déconnecter"):
    st.session_state.clear()
    try:
        cookie.remove("auth")
    except AttributeError:
        pass  # Ignore si la méthode n'existe pas
    st.rerun()

with st.sidebar:
    # Footer dans la sidebar
    st.sidebar.markdown("""
        <div style="
            position: fixed;
            bottom: 0;
            padding: 10px 20px;
            background: inherit;
            color: #7f8c8d;
            font-size: 0.8em;
            text-align: center;
        ">
            Price Scope 2025 - Tous droits réservés
        </div>
    """, unsafe_allow_html=True)
