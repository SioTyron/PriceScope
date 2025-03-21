import streamlit as st
from function import *
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
    bdd_url = "http://localhost:8888/phpMyAdmin5/index.php?route=/table/change&db=Price_Scope&table=articles"
    st.title("📊 Analyse des Prix Grande Distribution")
    # Gestion des dates
    with st.expander("🔧 Paramètres de Période", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            start_date = pd.to_datetime("2024-01-01")
            end_date = pd.to_datetime("2025-03-31")
            date_range = st.date_input(
                "Sélectionnez la plage d'analyse",
                [start_date, end_date],
                help="Sélectionnez une période entre 2024-01-01 et 2025-03-31"
            )
            
        start_date, end_date = date_range
        if start_date > end_date:
            st.error("⚠️ Erreur de période : La date de début doit être antérieure à la date de fin.")
            return

    # Connexion base de données
    connection = connect_to_db()
    if not connection:
        st.error("🚨 Échec de connexion à la base de données")
        return
    
    st.success(f"✅ Données chargées ({start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')})")
    
    # Affichage des données brutes
    if st.checkbox("📁 Afficher les données brutes"):
        data = fetch_commerce(connection, start_date, end_date)
        filtered_data = fetch_commerce_filtered(connection, start_date, end_date)
        
        tab1, tab2 = st.tabs(["Données complètes", "Données filtrées"])
        with tab1:
            st.dataframe(data.style.highlight_max(color='#4CAF50', axis=0), use_container_width=True)
        with tab2:
            st.dataframe(filtered_data.style.format({"prixTtc": "€{:.2f}"}), use_container_width=True)

    # Ajout d'un article
    if st.session_state["role"] in ["editeur", "admin"]:
        st.link_button("⛁ Ajouter un article", bdd_url, help=None, type="secondary", icon=None, disabled=False, use_container_width=False)
        log_action(st.session_state["user_id"], "Ajout d'un article")
    
    # Analyse par catégorie
    st.header("📈 Analyse par Catégorie")
    categories = fetch_product_categories(connection)
    
    for category in categories:
        with st.container():
            # Création d'une clé unique pour chaque catégorie
            if f"show_chart_{category}" not in st.session_state:
                st.session_state[f"show_chart_{category}"] = False
            
            st.markdown('<div class="category-container">', unsafe_allow_html=True)
            st.subheader(f"🏷️ {category}")
            products = fetch_products_by_category(connection, category)
            
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                selected_product = st.selectbox(
                    f"Sélection produit ({category})",
                    products,
                    key=f"{category}_product"
                )
            with col2:
                period = st.selectbox(
                    "Période de comparaison",
                    ["Aucun", "Mois -1", "Année -1"],
                    key=f"{selected_product}_period"
                )
                
            # Métriques de prix
            if selected_product:
                display_product_price(connection, start_date, end_date, selected_product, period)
            
            # Bouton toggle pour le graphique
            col1, col2 = st.columns([3, 1])
            with col1:
                btn_label = "📉 Masquer l'évolution des prix" if st.session_state[f"show_chart_{category}"] else "📈 Afficher l'évolution des prix"
                if st.button(btn_label, key=f"toggle_{category}"):
                    st.session_state[f"show_chart_{category}"] = not st.session_state[f"show_chart_{category}"]
            
            # Affichage conditionnel du graphique
            if st.session_state[f"show_chart_{category}"]:
                with st.spinner("Chargement du graphique..."):
                    price_evolution_df = fetch_price_evolution(connection, selected_product)
                    if not price_evolution_df.empty:
                        fig = px.line(
                            price_evolution_df,
                            x='date_Achat',
                            y='prixTtc',
                            markers=True,
                            title=f"Historique des prix - {selected_product}",
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
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)  # Espace supplémentaire entre les catégories

def display_product_price(connection, start_date, end_date, selected_product, period):
    """Affichage des métriques de prix pour un produit"""
    current_price = fetch_product_price(connection, selected_product, start_date, end_date)
    
    if period != "Aucun":
        delta = calculate_price_delta(connection, selected_product, start_date, end_date, period)
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
    current_price = fetch_product_price(connection, selected_product, start_date, end_date)
    min_price = fetch_min_price(connection, selected_product, start_date, end_date)
    max_price = fetch_max_price(connection, selected_product, start_date, end_date)
    
    with col2:
        st.metric("Prix Minimum", f"{min_price:.2f} €")
    with col3:
        st.metric("Prix Maximum", f"{max_price:.2f} €")

def calculate_price_delta(connection, product, start_date, end_date, period):
    """Calcul de la variation de prix par rapport à une période précédente"""
    if period == "Mois -1":
        offset = pd.DateOffset(months=1)
    elif period == "Année -1":
        offset = pd.DateOffset(years=1)
    else:
        return None
    
    previous_start = start_date - offset
    previous_end = end_date - offset
    previous_price = fetch_product_price(connection, product, previous_start, previous_end)
    current_price = fetch_product_price(connection, product, start_date, end_date)
    
    if previous_price and current_price:
        return f"{(current_price - previous_price):.2f} €"
    return None

if __name__ == "__main__":
    main()