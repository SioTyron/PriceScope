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
def display_product_price():
    connection = connect_to_db()
    
    product_names = fetch_product_names(connection)
    
    with st.expander("Selectionez un produit"):
        selected_product = st.selectbox("Produits", product_names)
    
    if selected_product:
        price = fetch_product_price(connection, selected_product)
        if price is not None:
            st.markdown("""
                <style>
                .metric-container {
                    background-color: black;
                    padding: 10px;
                    border-radius: 5px;
                    text-align: center;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    border: 2px solid white;
                }
                .metric-title {
                    color: #4CAF50;
                    font-size: 18px;
                    font-weight: bold;
                }
                .metric-value {
                    font-size: 24px;
                    font-weight: bold;
                }
                </style>
                <div class="metric-container">
                    <div class="metric-title">Prix</div>
                    <div class="metric-value">"""f"{price} €""""</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.write("Prix non trouvé.")

# Appel de la fonction pour afficher le prix du produit
display_product_price()
