import streamlit as st
from function_fastfood import *
from connexion import *
import plotly.express as px
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import yagmail


st.title("📑 Test Page")
st.write("Cette page est destionée aux administrateurs, elle permet le test des nouvelles fonctionnalités.")

#Code de la page après vérification des droits requis
if st.session_state["role"] in ["admin"]:
    st.success("Vous êtes administrateur.")
    st.write("Vous avez accès à cette page.")
    st.write("Voici les données de la base de données:")
    connection = connect_to_db()


    # Configuration de votre email pour l'envoi (via Yagmail)

    EMAIL_SENDER = st.secrets["gmail_credential"]["mail_sender"]
    EMAIL_PASSWORD = st.secrets["gmail_credential"]["mail_password"]
    EMAIL_RECEIVER = st.secrets["gmail_credential"]["mail_receiver"]

    st.title("Demande d'ajout d'article")
    st.subheader("Vos demandes feront l'objet d'une vérification avant d'être ajoutées à la base de données.")

    # Initialiser les valeurs par défaut des champs dans Session State
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "email" not in st.session_state:
        st.session_state.email = ""
    if "libelle" not in st.session_state:
        st.session_state.libelle = ""
    if "nom" not in st.session_state:
        st.session_state.nom = ""
    if "commune" not in st.session_state:
        st.session_state.commune = ""
    if "pays" not in st.session_state:
        st.session_state.pays = ""
    if "date_achat" not in st.session_state:
        st.session_state.date_achat = None
    if "nom_enseigne" not in st.session_state:
        st.session_state.nom_enseigne = ""
    if "cate_enseigne" not in st.session_state:
        st.session_state.cate_enseigne = ""
    if "prix" not in st.session_state:
        st.session_state.prix = 0.0
    if "message" not in st.session_state:
        st.session_state.message = ""
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    # Formulaire Streamlit
    with st.form("upload_form"):
        name = st.text_input("Votre nom", value=st.session_state.name)
        email = st.text_input("Votre email", value=st.session_state.email)
        libelle = st.text_input("Libellé de l'article", value=st.session_state.libelle)
        nom = st.text_input("Nom de l'article", value=st.session_state.nom)
        commune = st.text_input("Commune d'achat", value=st.session_state.commune)
        pays = st.text_input("Pays d'achat", value=st.session_state.pays)
        date_achat = st.date_input("Date d'achat", value=st.session_state.date_achat)
        nom_enseigne = st.text_input("Nom de l'enseigne", value=st.session_state.nom_enseigne)
        cate_enseigne = st.text_input("Catégorie de l'enseigne ex: fastfood, grande distribution", value=st.session_state.cate_enseigne)
        prix = st.number_input("Prix de l'article", value=st.session_state.prix)
        uploaded_file = st.file_uploader("Téléchargez une preuve de l'achat (ticket...)", type=["png", "jpg", "jpeg", "pdf"])
        message = st.text_area("Commentaire", value=st.session_state.message)
        submit_button = st.form_submit_button("Envoyer")

    # Traitement après soumission
    if submit_button:
        # Vérification des champs obligatoires
        if not name or not email or not libelle or not nom or not commune or not pays or not date_achat or not nom_enseigne or not cate_enseigne or prix <= 0:
            st.error("Veuillez remplir les champs obligatoires : 'Nom', 'Email', 'Libellé', 'Nom Article', 'Commune', 'Pays', 'Date d'achat', 'Nom de l'enseigne', 'Catégorie de l'enseigne', 'Prix'.")
        elif uploaded_file is None:
            st.warning("Veuillez télécharger un fichier avant de soumettre le formulaire.")
        else:
            # Enregistrer temporairement le fichier
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Envoi de l'email avec Yagmail
            try:
                yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)
                yag.send(
                    to=EMAIL_RECEIVER,
                    subject=f"Demande d'ajout d'articles de : {name}",
                    contents=f"Nom : {name}\nEmail : {email}\nLibellé : {libelle}\nNom de l'article : {nom}\nCommune : {commune}\nPays : {pays}\nDate d'achat : {date_achat}\nNom de l'enseigne : {nom_enseigne}\nCatégorie : {cate_enseigne}\nPrix : {prix}\nMessage : {message}",
                    attachments=[uploaded_file.name]
                )

                st.success("Formulaire envoyé avec succès !")

                # Réinitialisation des champs après envoi
                st.session_state.name = ""
                st.session_state.email = ""
                st.session_state.libelle = ""
                st.session_state.nom = ""
                st.session_state.commune = ""
                st.session_state.pays = ""
                st.session_state.date_achat = None
                st.session_state.nom_enseigne = ""
                st.session_state.cate_enseigne = ""
                st.session_state.prix = 0.0
                st.session_state.message = ""
                st.session_state.uploaded_file = None
            except Exception as e:
                st.error(f"Une erreur s'est produite lors de l'envoi de l'email : {str(e)}")

else :
    st.error("Vous n'avez pas accès à cette page.")