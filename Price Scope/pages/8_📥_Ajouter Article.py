import streamlit as st
from function_grandedistribution import *
from connexion import *
import plotly.express as px
import pandas as pd
import yagmail
from auth_utils import *

if not st.session_state.get("authenticated", False):
    st.warning("Vous devez être connecté pour accéder à cette page.")
    st.stop()

# Configuration de la page
st.set_page_config(page_title="📥 Ajouter un Article", layout="wide")
st.title("📥 Ajouter un Article")
st.subheader("Comment Ajouter un Article ?")
with st.expander("📄 Instructions"):
    st.write("""<h3>✨ Merci de contribuer à l'amélioration de Price Scope !</h3>
    <p>
        Vous souhaitez participer au développement de <strong>Price Scope</strong> en ajoutant un nouvel article ? Pour cela, veuillez remplir le formulaire ci-dessous.
    </p>
    <h4>⚠️ Points importants à retenir :</h4>
    <ul>
        <li>🛍️ <strong>Preuve d'achat obligatoire</strong> : Chaque demande doit être accompagnée d'une pièce jointe justifiant l'achat de l'article (ex. 🧾 ticket de caisse) aux formats png, jpg, jpeg, pdf.</li>
        <li>🔎 <strong>Vérification des demandes</strong> : Votre soumission sera examinée par un administrateur avant d'être ajoutée à la base de données.</li>
        <li>✅ <strong>Fiabilité garantie</strong> : Ce processus nous permet d'assurer l'intégrité des données et de garantir la fiabilité des informations partagées sur <strong>Price Scope</strong>.</li>
        <li>📧 <strong>Notification par email</strong> : Vous serez informé par email dès que votre demande aura été validée.</li>
    </ul>
    <p>🎉 <em>Nous vous remercions pour votre contribution précieuse à notre communauté !</em></p>
""",unsafe_allow_html=True)
    
def fetch_fastfood_categories(connection):
    query = "SELECT DISTINCT nom_Enseigne FROM `articles` WHERE categorie_Enseigne = 'Fast Food'"
    categories_df = pd.read_sql(query, connection)
    return categories_df['nom_Enseigne'].tolist()
  
# Configuration de votre email pour l'envoi (via Yagmail)

EMAIL_SENDER = st.secrets["gmail_credential"]["mail_sender"]
EMAIL_PASSWORD = st.secrets["gmail_credential"]["mail_password"]
EMAIL_RECEIVER = st.secrets["gmail_credential"]["mail_receiver"]

st.subheader("Demande d'ajout d'article")
st.write("Vos demandes feront l'objet d'une vérification avant d'être ajoutées à la base de données.")

# Initialiser les valeurs par défaut des champs dans Session State
if "name" not in st.session_state:
    st.session_state.name = ""
if "email" not in st.session_state:
    st.session_state.email = ""
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

#Initialiser les valeurs par défaut des champs dans Session State pour le formulaire de plusieurs articles
if "email2" not in st.session_state:
    st.session_state.email2 = ""
if "commune2" not in st.session_state:
    st.session_state.commune2 = ""
if "pays2" not in st.session_state:
    st.session_state.pays2 = ""
if "date_achat2" not in st.session_state:
    st.session_state.date_achat2 = None
if "nom_enseigne2" not in st.session_state:
    st.session_state.nom_enseigne2 = ""
if "cate_enseigne2" not in st.session_state:
    st.session_state.cate_enseigne2 = ""
if "message2" not in st.session_state:
    st.session_state.message2 = ""
if "uploaded_file2" not in st.session_state:
    st.session_state.uploaded_file2 = None

with st.expander("📋 Ajouter 1 Article", expanded=True):
    # Formulaire Streamlit
    with st.form("upload_form"):
        #name = st.text_input("Votre nom", value=st.session_state.name)
        email = st.text_input("Votre email*", value=st.session_state.email)
        #libelle = st.text_input("Libellé de l'article", value=st.session_state.libelle)
        nom = st.text_input("Nom de l'article*", value=st.session_state.nom)
        commune = st.text_input("Commune d'achat*", value=st.session_state.commune)
        pays = st.text_input("Pays d'achat*", value=st.session_state.pays)
        date_achat = st.date_input("Date d'achat*", value=st.session_state.date_achat)
        nom_enseigne = st.text_input("Nom de l'enseigne*", value=st.session_state.nom_enseigne)
        cate_enseigne = st.text_input("Catégorie de l'enseigne ex: fastfood, grande distribution*", value=st.session_state.cate_enseigne)
        prix = st.number_input("Prix de l'article*", value=st.session_state.prix)
        uploaded_file = st.file_uploader("Téléchargez une preuve de l'achat (ticket...)*", type=["png", "jpg", "jpeg", "pdf"])
        message = st.text_area("Commentaire", value=st.session_state.message)
        submit_button = st.form_submit_button("Envoyer")

    # Traitement après soumission
    if submit_button:
        # Vérification des champs obligatoires
        if not email or not nom or not commune or not pays or not date_achat or not nom_enseigne or not cate_enseigne or prix <= 0:
            st.error("Veuillez remplir les champs obligatoires : 'Nom', 'Email', 'Nom Article', 'Commune', 'Pays', 'Date d'achat', 'Nom de l'enseigne', 'Catégorie de l'enseigne', 'Prix'.")
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
                        subject=f"Demande d'ajout d'article (x1) : {email}",
                        contents=f"Email : {email}\nNom de l'article : {nom}\nCommune : {commune}\nPays : {pays}\nDate d'achat : {date_achat}\nNom de l'enseigne : {nom_enseigne}\nCatégorie : {cate_enseigne}\nPrix : {prix}\nMessage : {message}",
                        attachments=[uploaded_file.name]
                    )

                    st.success("Formulaire envoyé avec succès !")

                    # Réinitialisation des champs après envoi
                    st.session_state.email = ""
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

with st.expander("📋 Ajouter Plusieurs Articles", expanded=True):
    # Formulaire Streamlit
    with st.form("group_form"):
        email2 = st.text_input("Votre email*", value=st.session_state.email2)
        commune2 = st.text_input("Commune d'achat*", value=st.session_state.commune2)
        pays2 = st.text_input("Pays d'achat*", value=st.session_state.pays2)
        date_achat2 = st.date_input("Date d'achat*", value=st.session_state.date_achat2)
        nom_enseigne2 = st.text_input("Nom de l'enseigne*", value=st.session_state.nom_enseigne2)
        cate_enseigne2 = st.text_input("Catégorie de l'enseigne ex: fastfood, grande distribution*", value=st.session_state.cate_enseigne2)
        uploaded_file2 = st.file_uploader("Téléchargez une preuve de l'achat (ticket...)*", type=["png", "jpg", "jpeg", "pdf"])
        message2 = st.text_area("Commentaire", value=st.session_state.message2)
        submit_button2 = st.form_submit_button("Envoyer")

    # Traitement après soumission
    if submit_button2:
        # Vérification des champs obligatoires
        if not email2 or not commune2 or not pays2 or not date_achat2 or not nom_enseigne2 or not cate_enseigne2 :
            st.error("Veuillez remplir les champs obligatoires : 'Email', 'Commune', 'Pays', 'Date d'achat', 'Nom de l'enseigne', 'Catégorie de l'enseigne'.")
        elif uploaded_file2 is None:
            st.warning("Veuillez télécharger un fichier avant de soumettre le formulaire.")
        else:
            # Enregistrer temporairement le fichier
            with open(uploaded_file2.name, "wb") as f:
                f.write(uploaded_file2.getbuffer())

            # Envoi de l'email avec Yagmail
                try:
                    yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)
                    yag.send(
                        to=EMAIL_RECEIVER,
                        subject=f"Demande d'ajout de plusieurs articles : {email2}",
                        contents=f"Email : {email2}\nCommune : {commune2}\nPays : {pays2}\nDate d'achat : {date_achat2}\nNom de l'enseigne : {nom_enseigne2}\nCatégorie : {cate_enseigne2}\nMessage : {message2}",
                        attachments=[uploaded_file2.name]
                    )

                    st.success("Formulaire envoyé avec succès !")

                    # Réinitialisation des champs après envoi
                    st.session_state.email2 = ""
                    st.session_state.commune2 = ""
                    st.session_state.pays2 = ""
                    st.session_state.date_achat2 = None
                    st.session_state.nom_enseigne2 = ""
                    st.session_state.cate_enseigne2 = ""
                    st.session_state.message2 = ""
                    st.session_state.uploaded_file2 = None
                except Exception as e:
                    st.error(f"Une erreur s'est produite lors de l'envoi de l'email : {str(e)}")


if st.sidebar.button("Se déconnecter"):
    st.session_state.clear()
    try:
        cookie.remove("auth")
    except AttributeError:
        pass  # Ignore si la méthode n'existe pas
    st.rerun()

with st.sidebar:
    # Footer dans la sidebar
    st.sidebar.markdown("""
        <div style="
            position: fixed;
            bottom: 0;
            padding: 10px 20px;
            background: inherit;
            color: #7f8c8d;
            font-size: 0.8em;
            text-align: center;
        ">
            Price Scope 2025 - Tous droits réservés
        </div>
    """, unsafe_allow_html=True)