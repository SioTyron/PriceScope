import streamlit as st

st.title("☏ Contact")

st.markdown("""
    <style>
         .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }

        form {
            display: flex;
            flex-direction: column;
            max-width: 400px;
            margin: 0 auto;
            width: 100%;
        }
        input, textarea, button {
            margin-bottom: 1rem;
            padding: 0.5rem;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)


contact_form = """
            <div class="centered">
                <h2>Vous souhaitez nous contacter ?</h2><br/>
                <form
                action="https://formspree.io/f/moveddzq"
                method="POST">
                <input type="text" name="name" placeholder="Votre Nom" required>
                <input type="email" name="email" placeholder="Votre Email" required>
                <textarea name="message"placeholder="Votre Message" required></textarea>
                <button type="submit">Envoyer</button>
                </form>
            </div>

             """

st.markdown(contact_form, unsafe_allow_html=True)
