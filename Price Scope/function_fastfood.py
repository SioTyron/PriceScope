import pandas as pd
from connexion import connect_to_db

# Récupérer les données des Fast Food
def fetch_fastfood(connection, start_date, end_date):
    query = f"""
    SELECT * FROM `articles`
    WHERE date_Achat BETWEEN '{start_date}' AND '{end_date}' AND categorie_Enseigne = 'Fast Food'
    """
    return pd.read_sql(query, connection)

def fetch_fastfood_filtered(connection, start_date, end_date):
    query = f"""
    SELECT id_Article, nom_Article, nom_Enseigne, prixTtc, date_Achat, Commune FROM `articles`
    WHERE date_Achat BETWEEN '{start_date}' AND '{end_date}' AND categorie_Enseigne = 'Fast Food'
    """
    filtered_df = pd.read_sql(query, connection)
    return filtered_df

def fetch_fastfood_price(connection, product_name, start_date, end_date):
    query = f"""
    SELECT prixTtc FROM `articles`
    WHERE nom_Article = '{product_name}' AND date_Achat BETWEEN '{start_date}' AND '{end_date}'
    """
    price_df = pd.read_sql(query, connection)
    return price_df['prixTtc'].iloc[0] if not price_df.empty else None

def fetch_fastfood_categories(connection):
    query = "SELECT DISTINCT nom_Enseigne FROM `articles` WHERE categorie_Enseigne = 'Fast Food'"
    categories_df = pd.read_sql(query, connection)
    return categories_df['nom_Enseigne'].tolist()

def fetch_fastfood_product_by_nameEnseigne(connection, category):
    """Récupère les produits d'une catégorie pour séparer l'affichage des produits"""
    query = f"""
    SELECT DISTINCT nom_Article, nom_Enseigne, Commune
    FROM `articles`
    WHERE nom_Enseigne = '{category}'
    """
    products_df = pd.read_sql(query, connection)
    return products_df

def fetch_price_evolution(connection, product_name):
    """Récupère l'évolution du prix d'un produit"""
    query = f"""
    SELECT date_Achat, prixTtc FROM `articles`
    WHERE nom_Article = '{product_name}'
    ORDER BY date_Achat
    """
    price_evolution_df = pd.read_sql(query, connection)
    return price_evolution_df

def fetch_min_price(connection, product_name, start_date, end_date):
    """Récupère le prix minimum historique pour un produit sur une période"""
    query = f"""
    SELECT MIN(prixTtc) as min_price FROM `articles`
    WHERE nom_Article = '{product_name}' AND date_Achat BETWEEN '{start_date}' AND '{end_date}'
    """
    min_price_df = pd.read_sql(query, connection)
    return min_price_df['min_price'].iloc[0] if not min_price_df.empty else None

def fetch_max_price(connection, product_name, start_date, end_date):
    """Récupère le prix maximum historique pour un produit sur une période"""
    query = f"""
    SELECT MAX(prixTtc) as max_price FROM `articles`
    WHERE nom_Article = '{product_name}' AND date_Achat BETWEEN '{start_date}' AND '{end_date}'
    """
    max_price_df = pd.read_sql(query, connection)
    return max_price_df['max_price'].iloc[0] if not max_price_df.empty else None

# Version améliorée de fetch_fastfood_price avec gestion d'erreur
def fetch_fastfood_price(connection, product_name, start_date, end_date):
    """Récupère le prix moyen d'un produit sur une période"""
    query = f"""
    SELECT AVG(prixTtc) as avg_price FROM `articles`
    WHERE nom_Article = '{product_name}' AND date_Achat BETWEEN '{start_date}' AND '{end_date}'
    """
    avg_price_df = pd.read_sql(query, connection)
    return avg_price_df['avg_price'].iloc[0] if not avg_price_df.empty else None