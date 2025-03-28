import streamlit as st
from function_grandedistribution import *
from connexion import *
import plotly.express as px
import pandas as pd

if not st.session_state.get("authenticated", False):
    st.warning("Vous devez être connecté pour accéder à cette page.")
    st.stop()

# Configuration de la page
st.set_page_config(page_title="🛒 Analytics Grande Distribution", layout="wide")

# Style personnalisé CSS
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    h1 {color: #2c3e50;}
    .category-container {margin-bottom: 3rem; padding: 1.5rem; ; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .block-container {padding-top: 1rem;}
    .stMetric {border-left: 4px solid #4CAF50; padding: 15px;}
    .plot-container {border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 1rem;}
    .stAlert {border-radius: 10px;}
    .toggle-button {margin-top: 1rem;}
    </style>
    """, unsafe_allow_html=True)

def main():
    connection = connect_to_db()
    if not connection:
        st.error("🚨 Échec de connexion à la base de données")
        return

    st.header("📈 Analyse par Catégorie")
    categories = fetch_product_categories(connection)
    
    for idx, category in enumerate(categories):  # Ajout d'un index pour garantir des clés uniques
        with st.container():
            # Création d'une clé unique pour chaque catégorie
            if f"show_chart_{category}" not in st.session_state:
                st.session_state[f"show_chart_{category}"] = False
            
            st.markdown('<div class="category-container">', unsafe_allow_html=True)
            st.subheader(f"🏷️ {category}")
            
            # Récupérer les produits et les enseignes pour la catégorie
            products_df = fetch_products_by_category(connection, category)
            
            if not products_df.empty:
                col1, col2 = st.columns([2, 1])
                with col1:
                    # Sélection du produit
                    selected_product = st.selectbox(
                        f"Sélectionnez un produit dans la catégorie {category}",
                        products_df.apply(
                            lambda row: f"{row['nom_Article']} ({row['nom_Enseigne']}, {row['Commune']})",
                            axis=1
                        ),
                        key=f"{category}_{idx}_product"  # Inclure l'index dans la clé pour la rendre unique
                    )
                
                # Extraire les informations du produit sélectionné
                product_details = selected_product.split(" (Enseigne : ")
                product_name = product_details[0]
                enseigne_details = product_details[1].rstrip(")").split(", Commune : ")
                enseigne_name = enseigne_details[0]
                commune_name = enseigne_details[1]
                
                with col2:
                    # Sélection de la période de comparaison
                    period = st.selectbox(
                        "Période de comparaison",
                        ["Aucun", "Mois -1", "Année -1"],
                        key=f"{category}_{idx}_{selected_product}_period"  # Inclure l'index et le produit dans la clé
                    )
                
                # Métriques de prix
                if selected_product:
                    display_product_price(connection, product_name, enseigne_name, commune_name, period)
                
                # Bouton toggle pour le graphique
                btn_label = "📉 Masquer l'évolution des prix" if st.session_state[f"show_chart_{category}"] else "📈 Afficher l'évolution des prix"
                if st.button(btn_label, key=f"toggle_{category}_{idx}"):  # Inclure l'index dans la clé
                    st.session_state[f"show_chart_{category}"] = not st.session_state[f"show_chart_{category}"]
                
                # Affichage conditionnel du graphique
                if st.session_state[f"show_chart_{category}"]:
                    with st.spinner("Chargement du graphique..."):
                        price_evolution_df = fetch_price_evolution(connection, product_name, enseigne_name, commune_name)
                        if not price_evolution_df.empty:
                            fig = px.line(
                                price_evolution_df,
                                x='date_Achat',
                                y='prixTtc',
                                markers=True,
                                title=f"Historique des prix - {product_name} ({enseigne_name})",
                                labels={'prixTtc': 'Prix TTC (€)', 'date_Achat': 'Date'},
                                color_discrete_sequence=['#4CAF50']
                            )
                            fig.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                hovermode="x unified",
                                xaxis_title="",
                                yaxis_title="Prix (€)",
                                margin=dict(l=20, r=20, t=40, b=20)
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("Aucune donnée historique disponible")
            else:
                st.warning(f"Aucun produit trouvé pour la catégorie {category}.")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)  # Espace supplémentaire entre les catégories

def display_product_price(connection, product_name, enseigne_name, commune_name, period):
    """Affichage des métriques de prix pour un produit"""
    start_date = pd.to_datetime("2024-01-01")
    end_date = pd.to_datetime("2025-03-31")
    
    current_price = fetch_product_price(connection, product_name, enseigne_name, commune_name, start_date, end_date)
    
    if period != "Aucun":
        delta = calculate_price_delta(connection, product_name, enseigne_name, commune_name, start_date, end_date, period)
        delta_color = "inverse"  # Auto-couleur selon valeur
    else:
        delta = None
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Prix Actuel Moyen",
            value=f"{current_price:.2f} €" if current_price else "N/A",
            delta=delta,
            help="Variation par rapport à la période précédente"
        )
    min_price = fetch_min_price(connection, product_name, enseigne_name, commune_name, start_date, end_date)
    max_price = fetch_max_price(connection, product_name, enseigne_name, commune_name, start_date, end_date)
    
    with col2:
        st.metric("Prix Minimum", f"{min_price:.2f} €")
    with col3:
        st.metric("Prix Maximum", f"{max_price:.2f} €")


def calculate_price_delta(connection, product_name, enseigne_name, commune_name, start_date, end_date, period):
    """Calcul de la variation de prix par rapport à une période précédente"""
    if period == "Mois -1":
        offset = pd.DateOffset(months=1)
    elif period == "Année -1":
        offset = pd.DateOffset(years=1)
    else:
        return None
    
    # Calcul des dates pour la période précédente
    previous_start = start_date - offset
    previous_end = end_date - offset
    
    # Récupérer les prix pour la période précédente et la période actuelle
    previous_price = fetch_product_price(connection, product_name, enseigne_name, commune_name, previous_start, previous_end)
    current_price = fetch_product_price(connection, product_name, enseigne_name, commune_name, start_date, end_date)
    
    # Calcul de la variation
    if previous_price and current_price:
        return f"{(current_price - previous_price):.2f} €"
    return None

if __name__ == "__main__":
    main()
