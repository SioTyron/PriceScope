import streamlit as st
from function import *
from connexion import *

st.title("🛒 Grande Distribution")

# Plage de dates
start_date = pd.to_datetime("2024-01-01")
end_date = pd.to_datetime("2025-03-31") #Limité au 31 mars 2025 pour la version test

# Utiliser le widget date_input pour sélectionner une plage de dates
date_range = st.date_input("Sélectionnez la plage de dates", [start_date, end_date])

# Extraire les dates de début et de fin
start_date = date_range[0]
end_date = date_range[1]

if start_date > end_date:
    st.error("La date de début doit être antérieure à la date de fin.")
else:
    connection = connect_to_db()


if connection:
    st.success(f"Éléments chargés pour la période du : {start_date} au {end_date}")
    if st.checkbox("Afficher le DF"):
        data = fetch_commerce(connection, start_date, end_date)
        filtered_data  = fetch_commerce_filtered(connection, start_date,end_date)
        if not data.empty:
            st.write("")
            st.write(data)
            st.write(filtered_data)
        else:
            st.warning("Aucune donnée trouvée dans la plage de dates sélectionnée.")
            connection.close()
else:
    st.error("Échec de la connexion à la base de données.")

# Fonction pour afficher le prix du produit dans un metric
import streamlit as st
import pandas as pd

def display_product_price(connection, start_date, end_date):
    # CSS personnalisé uniquement pour les metrics
    st.markdown("""
    <style>
        /* Style principal uniquement pour les cartes de metrics */
        div[data-testid="stMetric"] {
            background-color: #black;  
            border: 1px solid #B3D7F2;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            margin: 10px 0;
        }

        /* Cible spécifiquement les éléments à l'intérieur du metric */
        div[data-testid="stMetric"] > div {
            justify-content: space-between;
        }

        div[data-testid="stMetric"] label {
            font-size: 1.1rem !important;
            color: #6C757D !important;
            font-weight: 500 !important;
        }

        /* Style spécifique à la valeur numérique */
        div[data-testid="stMetric"] .st-b7 {
            color: #2C3E50 !important;
            font-size: 1.8rem !important;
            font-weight: bold !important;
        }

        /* Style pour le delta en ciblant uniquement dans les metrics */
        div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
            font-size: 1rem !important;
            font-weight: 500 !important;
            align-items: center !important;
        }

        /* Cache les icônes SVG par défaut */
        div[data-testid="stMetric"] [data-testid="stMetricDelta"] svg {
            display: none !important;
        }

        /* Animation au survol uniquement pour les metrics */
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

    selected_product = st.selectbox("Selectionnez un produit", fetch_product_names(connection))
    period = st.selectbox("Selectionnez une période pour comparer les prix", ["Aucun", "Mois -1", "Année -1"])

    current_price = fetch_product_price(connection, selected_product, start_date, end_date)

    if period == "Mois -1":
        period_start_date = start_date - pd.DateOffset(months=1)
        period_end_date = end_date - pd.DateOffset(months=1)
    elif period == "Année -1":
        period_start_date = start_date - pd.DateOffset(years=1)
        period_end_date = end_date - pd.DateOffset(years=1)
    else:
        period_start_date = start_date
        period_end_date = end_date

    period_price = fetch_product_price(connection, selected_product, period_start_date, period_end_date) if period_start_date and period_end_date else None

    if current_price is not None:
        if period_price is not None and period != "Aucun":
            price_difference = current_price - period_price
            percentage_change = (price_difference / period_price) * 100
            
            delta_color = "inverse" if current_price > period_price else "normal"
            delta_emoji = "▲" if current_price > period_price else "▼"
            delta_text = f"{delta_emoji} {abs(percentage_change):.2f}% > {period_price} €"

            st.metric(
                label="Prix Actuel",
                value=f"{current_price:.2f} €",
                delta=delta_text,
                delta_color=delta_color
            )
        else:
            st.metric(
                label="Prix Actuel",
                value=f"{current_price:.2f} €",
                delta="Aucune comparaison" if period == "Aucun" else "Données non disponibles"
            )
    else:
        st.error("Prix non trouvé pour la période sélectionnée.")

if connection:
    display_product_price(connection, start_date, end_date)