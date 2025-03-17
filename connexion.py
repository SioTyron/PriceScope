import streamlit as st
import mysql.connector
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Détails de la connexion à la base de données
db_config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'Price_Scope',
    'port': 8889
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
