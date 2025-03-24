import streamlit as st
import pandas as pd
from connexion import connect_to_db

if not st.session_state.get("authenticated", False):
    st.warning("Vous devez être connecté pour accéder à cette page.")
    st.stop()

if st.session_state["role"] not in ["editeur", "admin"]:
    st.warning("Vous n'avez pas les permissions nécessaires pour accéder à cette page.")
    st.stop()

st.set_page_config("Price Scope", page_icon="💶", layout="wide")

# Info statut app
connection = connect_to_db()
if connection:
    st.sidebar.success("Bienvenue sur Price Scope")
else:
    st.sidebar.error("Erreur lors du chargement de l'application")

# Récupérer les données de la base de données en fonction de la plage de dates
def fetch_data(connection, start_date, end_date):
    query = f"""
    SELECT * FROM `articles`
    WHERE date_Achat BETWEEN '{start_date}' AND '{end_date}'
    """
    return pd.read_sql(query, connection)

# Header
st.title("Data Gestion ⛁ ")

# Recharger le set Données
if st.button("Recharger le set de données"):
    st.popover("Fonction non implémentée", help=None, icon=None, disabled=True, use_container_width=False)

# Widgets pour sélectionner la plage de dates
# Définir les dates par défaut
start_date = pd.to_datetime("2024-01-01")
end_date = pd.to_datetime("2025-03-31")  # Limité au 31 mars 2025 pour la version test

# Utiliser le widget date_input pour sélectionner une plage de dates
date_range = st.date_input("Sélectionnez la plage de dates", [start_date, end_date])

# Extraire les dates de début et de fin
start_date, end_date = date_range

if start_date > end_date:
    st.error("La date de début doit être antérieure à la date de fin.")
else:
    connection = connect_to_db()
    if connection:
        st.success("Connexion à la base de données établie.")
        data = fetch_data(connection, start_date, end_date)
        if data is not None and not data.empty:
            st.write(data)
        else:
            st.warning("Aucune donnée trouvée dans la plage de dates sélectionnée.")
        connection.close()
    else:
        st.error("Échec de la connexion à la base de données.")