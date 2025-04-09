import streamlit as st
import mysql.connector
import pandas as pd
from connexion import *

# Récupérer les données de la grande distribution (Commerce)
def fetch_commerce(connection, start_date, end_date):
    query = f"""
    SELECT * FROM `articles`
    WHERE date_Achat BETWEEN '{start_date}' AND '{end_date}' 
      AND categorie_Enseigne != 'Fast Food'
    """
    df = pd.read_sql(query, connection)
    return df

def fetch_commerce_filtered(connection, start_date, end_date):
    query = f"""
    SELECT id_Article, nom_Article, nom_Enseigne, prixTtc, date_Achat, Commune 
    FROM `articles`
    WHERE date_Achat BETWEEN '{start_date}' AND '{end_date}' 
      AND categorie_Enseigne != 'Fast Food'
    """
    filtered_df = pd.read_sql(query, connection)
    return filtered_df

# Fonctions de la page Grande Distribution
def fetch_product_price(connection, product_name, enseigne_name, commune_name, start_date, end_date):
    """Récupère le prix moyen d'un produit sur une période"""
    query = f"""
    SELECT AVG(prixTtc) as avg_price 
    FROM `articles`
    WHERE nom_Article = '{product_name}' 
      AND nom_Enseigne = '{enseigne_name}'
      AND Commune = '{commune_name}'
      AND date_Achat BETWEEN '{start_date}' AND '{end_date}'
    """
    avg_price_df = pd.read_sql(query, connection)
    return avg_price_df['avg_price'].iloc[0] if not avg_price_df.empty else None

def fetch_product_categories(connection):
    """Récupère les catégories de produits"""
    query = """
    SELECT DISTINCT categorie_Rayon 
    FROM `articles`
    WHERE categorie_Enseigne != 'Fast Food'
    """
    categories_df = pd.read_sql(query, connection)
    return categories_df['categorie_Rayon'].tolist()

def fetch_products_by_category(connection, category):
    """Récupère les produits d'une catégorie pour séparer l'affichage des produits"""
    query = f"""
    SELECT DISTINCT nom_Article, nom_Enseigne, Commune
    FROM `articles`
    WHERE categorie_Rayon = '{category}' 
      AND categorie_Enseigne != 'Fast Food'
    """
    products_df = pd.read_sql(query, connection)
    return products_df

def fetch_price_evolution(connection, product_name, enseigne_name, commune_name):
    """Récupère l'évolution du prix d'un produit"""
    query = f"""
    SELECT date_Achat, prixTtc 
    FROM `articles`
    WHERE nom_Article = '{product_name}'
      AND nom_Enseigne = '{enseigne_name}'
      AND Commune = '{commune_name}'
    ORDER BY date_Achat
    """
    price_evolution_df = pd.read_sql(query, connection)
    return price_evolution_df

def fetch_min_price(connection, product_name, enseigne_name , commune_name, start_date, end_date):
    """Récupère le prix minimum historique pour un produit sur une période"""
    query = f"""
    SELECT MIN(prixTtc) AS prix_min 
    FROM `articles`
    WHERE nom_Article = '{product_name}' 
      AND nom_Enseigne = '{enseigne_name}'
      AND Commune = '{commune_name}'
      AND date_Achat BETWEEN '{start_date}' AND '{end_date}'
      AND categorie_Enseigne != 'Fast Food'
    """
    min_df = pd.read_sql(query, connection)
    return min_df['prix_min'].iloc[0] if not min_df.empty else 0.0

def fetch_max_price(connection, product_name,enseigne_name, commune_name, start_date, end_date):
    """Récupère le prix maximum historique pour un produit sur une période"""
    query = f"""
    SELECT MAX(prixTtc) AS prix_max 
    FROM `articles`
    WHERE nom_Article = '{product_name}' 
      AND nom_Enseigne = '{enseigne_name}'
      AND Commune = '{commune_name}'
      AND date_Achat BETWEEN '{start_date}' AND '{end_date}'
      AND categorie_Enseigne != 'Fast Food'
    """
    max_df = pd.read_sql(query, connection)
    return max_df['prix_max'].iloc[0] if not max_df.empty else 0.0


def fetch_last_price(connection, product_name, enseigne_name, commune_name, start_date, end_date):
    """Récupère le dernier prix enregistré pour un produit sur une période"""
    query = f"""
    SELECT prixTtc 
    FROM `articles`
    WHERE nom_Article = '{product_name}' 
      AND nom_Enseigne = '{enseigne_name}'
      AND Commune = '{commune_name}'
      AND date_Achat BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY date_Achat DESC
    LIMIT 1
    """
    last_price_df = pd.read_sql(query, connection)
    return last_price_df['prixTtc'].iloc[0] if not last_price_df.empty else None