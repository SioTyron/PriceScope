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

    st.title("📊 Analyse des Prix Grande Distribution")
  
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
                product_details = selected_product.split(" (")
                product_name = product_details[0]
                enseigne_details = product_details[1].rstrip(")").split(", ") 
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
    # Récupérer le dernier prix de l'article et sa date
    query = f"""
    SELECT prixTtc, date_Achat 
    FROM `articles`
    WHERE nom_Article = '{product_name}' 
      AND nom_Enseigne = '{enseigne_name}'
      AND Commune = '{commune_name}'
    ORDER BY date_Achat DESC
    LIMIT 1
    """
    last_price_df = pd.read_sql(query, connection)
    if last_price_df.empty:
        st.error("Aucun prix trouvé pour cet article.")
        return

    current_price = last_price_df['prixTtc'].iloc[0]
    last_date = pd.to_datetime(last_price_df['date_Achat'].iloc[0])

    # Calculer la variation de prix (delta) par rapport à la période de comparaison
    delta = None
    if period != "Aucun":
        delta_value = calculate_price_delta(connection, product_name, enseigne_name, commune_name, last_date, period, current_price)
        
        if delta_value is not None:
            # Déterminer la couleur et le symbole
            if delta_value > 0:
                delta_color = "inverse"  # Rouge pour augmentation
                delta_symbol = ""
            elif delta_value < 0:
                delta_color = "normal"   # Vert pour diminution
                delta_symbol = ""
            else:
                delta_color = "off"     # Pas de variation
                delta_symbol = ""
            
            # Formater le delta avec symbole et couleur
            delta = {
                "value": f"{abs(delta_value):.2f} € {delta_symbol}".strip(),
                "color": delta_color
            }

    # Définir une période historique complète pour les prix minimum et maximum
    historical_start_date = pd.to_datetime("2024-01-01")
    historical_end_date = last_date

    # Récupérer les prix minimum et maximum
    min_price = fetch_min_price(connection, product_name, enseigne_name, commune_name, historical_start_date, historical_end_date)
    max_price = fetch_max_price(connection, product_name, enseigne_name, commune_name, historical_start_date, historical_end_date)

    # Afficher les métriques
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_args = {
            "label": "Prix de l'Article",
            "value": f"{current_price:.2f} €",
            "help": "Prix le plus récent enregistré dans la base"
        }
        if delta:
            metric_args["delta"] = delta["value"]
            metric_args["delta_color"] = delta["color"]
        st.metric(**metric_args)
    
    with col2:
        st.metric("Prix Minimum", f"{min_price:.2f} €" if min_price else "N/A")
    with col3:
        st.metric("Prix Maximum", f"{max_price:.2f} €" if max_price else "N/A")

def calculate_price_delta(connection, product_name, enseigne_name, commune_name, last_date, period, current_price):
    """Calcul de la variation de prix par rapport à une période précédente"""
    if period == "Mois -1":
        # Calculer la période du mois précédent
        previous_start = (last_date - pd.DateOffset(months=1)).replace(day=1)
        previous_end = (last_date - pd.DateOffset(months=1)).replace(day=1) + pd.DateOffset(months=1) - pd.DateOffset(days=1)
    elif period == "Année -1":
        # Calculer la période de l'année précédente
        previous_start = last_date - pd.DateOffset(years=1)
        previous_end = last_date - pd.DateOffset(years=1) + pd.DateOffset(days=last_date.day - 1)
    else:
        return None

    # Récupérer le prix pour la période précédente
    previous_price = fetch_last_price(connection, product_name, enseigne_name, commune_name, previous_start, previous_end)

    # Calcul de la variation
    if previous_price is not None:
        return current_price - previous_price
    return None

if __name__ == "__main__":
    main()