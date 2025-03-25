import streamlit as st

st.title("🏠 Accueil")
# Ajout de styles CSS personnalisés
st.markdown("""
    <style>
        .title {
            font-size: 30px;
            font-weight: bold;
            color: #4CAF50;
        }
        .subtitle {
            font-size: 24px;
            color: #555;
        }
        .section {
            margin-top: 20px;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 8px;
        }
        .section h3 {
            color: #2C3E50;
        }
        .section p {
            color: #333;
        }
        .bullet {
            margin-left: 20px;
            color: #2C3E50;
        }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<div class="title">Price Scope 🧐</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Vos prix à la loupe</div>', unsafe_allow_html=True)

# Introduction
st.markdown("""
    <div class="section">
        <p>
            Bienvenue sur <b>Price Scope</b>, un outil puissant conçu pour analyser l'évolution des prix 
            des articles du quotidien. Ce projet a pour objectif de vous aider à mieux comprendre les fluctuations des prix, 
            afin de prendre des décisions éclairées et de mieux gérer votre budget.
        </p>
    </div>
""", unsafe_allow_html=True)

# Fonctionnalités
st.markdown("""
    <div class="section">
        <h3>🌟 Fonctionnalités</h3>
        <ul class="bullet">
            <li>Suivez l'évolution des prix des produits divers (Fast-Food, Grande Distribution, etc.).</li>
            <li>Analysez les tendances de marché à court et à long terme.</li>
            <li>Explorez des graphiques interactifs et des rapports détaillés sur les données collectées.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Objectif
st.markdown("""
    <div class="section">
        <h3>🎯 Pourquoi Price Scope a été créé ?</h3>
        <p>
            Nous savons que gérer un budget peut être complexe. Price Scope est là pour simplifier 
            votre accès aux informations sur les prix et vous offrir une meilleure visibilité pour optimiser vos dépenses quotidiennes.
        </p>
    </div>
""", unsafe_allow_html=True)

# Collaboration
st.markdown("""
    <div class="section">
        <h3>👥 Participez à rendre l'outil meilleur </h3>
        <p>
            Price Scope se base sur vos données enregistrées pour proposer des analyses pertinentes. Ainsi, en partageant le prix des articles que vous achetez, vous contribuez à améliorer la quantité et la qualité des analyses fournies par l'outil.
            Vous avez la possiblité d'ajouter un article en cliquant sur les boutons "Ajouter un article" dans les différentes pages de l'application si vous êtes "éditeur".
        </p>
    </div>
""", unsafe_allow_html=True)

# Technologies utilisées
st.markdown("""
    <div class="section">
        <h3>🛠️ Technologies utilisées</h3>
        <ul class="bullet">
            <li><b>Python</b> pour l'analyse et le traitement des données.</li>
            <li><b>Streamlit</b> pour une interface intuitive et fluide.</li>
            <li><b>Pandas</b> pour la gestion efficace des données.</li>
            <li><b>MySQL</b> pour un stockage des données robuste et performant.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Auteur
st.markdown("""
    <div class="section">
        <h3>👤 À propos de l'auteur</h3>
        <p>
            Développé par <b>Tyron</b>, un passionné de solutions technologiques qui simplifient la vie quotidienne. 
            Pour toute question ou suggestion, n'hésitez pas à me contacter à l'adresse suivante : 
            <a href="mailto:certificat.tyron@gmail.com">pricescope.contact@gmail.com</a>.
        </p>
    </div>
""", unsafe_allow_html=True)

