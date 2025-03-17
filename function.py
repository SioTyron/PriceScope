import streamlit as st
import mysql.connector
import pandas as pd
from connexion import *

connect_to_db()

# Récupérer les données des Fast Food
def fetch_fastfood(connection, start_date, end_date,):
    query = f"""
    SELECT * FROM `articles`
    WHERE date_achat BETWEEN '{start_date}' AND '{end_date}' AND categorie_Article = 'Fast Food'
    """
    df = pd.read_sql(query, connection)
    return df

# Récupérer les données de la grande distribution (Commerce)
def fetch_commerce(connection, start_date, end_date,):
    query = f"""
    SELECT * FROM `articles`
    WHERE date_achat BETWEEN '{start_date}' AND '{end_date}' AND categorie_Enseigne = 'Grande Distribution'
    """
    df = pd.read_sql(query, connection)
    return df

def fetch_commerce_filtered(connection, start_date, end_date,):
    query = f"""
    SELECT id_Article, nom_Article, nom_Enseigne, prixTtc, date_Achat, Commune FROM `articles`
    WHERE date_achat BETWEEN '{start_date}' AND '{end_date}' AND categorie_Enseigne = 'Grande Distribution'
    """
    filtered_df = pd.read_sql(query, connection)
    return filtered_df


## Fonctions de la page Grande Distribution
def fetch_product_names(connection):
    # Récupérer les noms des produits pour les articles de Janvier 2025
    query = f" SELECT DISTINCT nom_Article FROM `articles`"
    product_names_df = pd.read_sql(query, connection)
    df = pd.read_sql(query, connection)
    return product_names_df['nom_Article'].tolist()

def fetch_product_price(connection, product_name):
    # Récupérer le prix du produit 
    query = f"""
    SELECT prixTtc FROM `articles`
    WHERE nom_Article = '{product_name}' AND date_Achat BETWEEN '2024-01-01' AND '2025-01-31'
    """
    price_df = pd.read_sql(query, connection)
    return price_df['prixTtc'].iloc[0] if not price_df.empty else None