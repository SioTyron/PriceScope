import streamlit as st
from datetime import datetime
from connexion import *
from auth_utils import *


if "authenticated" not in st.session_state:
    check_auto_login()

if not st.session_state.get("authenticated", False):
    st.warning("Vous devez être connecté pour accéder à cette page.")
    st.stop()


st.title("🔔 Actualités")
st.write("Bienvenue sur la page des Actualités.")

# Fonctions CRUD
def add_post(title, content, author):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO posts (title, content, author, date_created) VALUES (%s, %s, %s, %s)",
        (title, content, author, datetime.now())
    )
    conn.commit()
    conn.close()

def get_all_posts():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts ORDER BY date_created DESC")
    posts = cursor.fetchall()
    conn.close()
    return posts

def get_post_by_id(post_id):
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    conn.close()
    return post

def update_post(post_id, title, content):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s WHERE id = %s",
        (title, content, post_id)
    )
    conn.commit()
    conn.close()

def delete_post(post_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    conn.commit()
    conn.close()

def news_page():
    # Vérification du rôle de l'utilisateur
    user_id = st.session_state.get("user_id")  # Assurez-vous que l'ID utilisateur est stocké dans la session
    if not user_id:
        st.warning("Vous devez être connecté pour accéder à cette page.")
        st.stop()

    user_role = get_role(user_id)  # Récupération du rôle de l'utilisateur
    is_admin = user_role == "admin"  # Vérifie si l'utilisateur est un administrateur

    # Section Admin
    if is_admin:
        st.header("Administration des actualités")

        # Formulaire d'ajout
        with st.expander("Nouvel article"):
            with st.form("add_post"):
                title = st.text_input("Titre")
                content = st.text_area("Contenu")
                if st.form_submit_button("Publier"):
                    add_post(title, content, "Admin")
                    st.success("Article publié !")

        # Gestion des articles existants
        st.subheader("Éditer/Supprimer des articles")
        posts = get_all_posts()
        
        for post in posts:
            with st.expander(f"{post['title']} - {post['date_created'].strftime('%d/%m/%Y')}"):
                with st.form(f"edit_{post['id']}"):
                    new_title = st.text_input("Titre", value=post['title'])
                    new_content = st.text_area("Contenu", value=post['content'])
                    col1, col2 = st.columns(2)
                    
                    if col1.form_submit_button("Mettre à jour"):
                        update_post(post['id'], new_title, new_content)
                        st.rerun()
                    
                    if col2.form_submit_button("Supprimer"):
                        delete_post(post['id'])
                        st.rerun()

# Affichage public
    else:
        posts = get_all_posts()
        
        if not posts:
            st.info("Aucune actualité disponible")
            
        for post in posts:
            # Container stylisé pour chaque article
            with st.container():
                st.markdown(f"""
                    <div style="
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        margin-bottom: 30px;
                        background: white;
                    ">
                        <h2 style="color: #2c3e50; margin-bottom: 8px;">{post['title']}</h2>
                        <p style="
                            color: #7f8c8d;
                            font-size: 0.9em;
                            margin-bottom: 15px;
                            font-style: italic;
                        ">
                            Publié le {post['date_created'].strftime('%d/%m/%Y à %H:%M')}
                        </p>
                        <div style="
                            color: #34495e;
                            line-height: 1.6;
                            font-size: 1em;
                        ">
                            {post['content']}
                    """, unsafe_allow_html=True)



if __name__ == "__main__":
    news_page()

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
