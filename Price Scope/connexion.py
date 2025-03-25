import streamlit as st
import mysql.connector
import streamlit_authenticator as stauth
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

def isConnected():
    if connect_to_db == None:
        print (False)
    else :
        print( True)

# Fonction pour enregistrer une action dans l'historique
def log_action(user_id, action):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO historique (user_id, action) VALUES (%s, %s)", (user_id, action))
        connection.commit()
        cursor.close()
        connection.close()