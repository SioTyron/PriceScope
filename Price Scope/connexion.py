import streamlit as st
import mysql.connector
import yaml
from yaml.loader import SafeLoader

# Détails de la connexion à la base de données
db_config = {
    'user': st.secrets["db_credentials"]["username"],
    'password': st.secrets["db_credentials"]["password"],
    'host': st.secrets["db_credentials"]["host"],
    'database': st.secrets["db_credentials"]["db_name"],
}

# Fonction pour se connecter à la base de données
def connect_to_db():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except mysql.connector.Error as err:
        st.error(f"Erreur de connexion : {err}")
        return None

# Vérifie si la connexion à la base de données est active
def isConnected():
    connection = connect_to_db()
    if connection is None:
        return False
    else:
        connection.close()
        return True

# Fonction pour enregistrer une action dans l'historique
def log_action(user_id, action):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO historique (user_id, action) VALUES (%s, %s)",
                (user_id, action)
            )
            connection.commit()
        except mysql.connector.Error as err:
            st.error(f"Erreur lors de l'enregistrement de l'action : {err}")
        finally:
            cursor.close()
            connection.close()

def get_role (user_id):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            if result:
                return result['role']
        except mysql.connector.Error as err:
            st.error(f"Erreur lors de la récupération du rôle : {err}")
        finally:
            cursor.close()
            connection.close()