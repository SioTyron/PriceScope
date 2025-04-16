import streamlit as st
from streamlit_cookies_controller import CookieController
from datetime import datetime

cookie = CookieController()

def check_auto_login():
    session_info = cookie.get("auth")
    if session_info and datetime.fromisoformat(session_info["expires_at"]) > datetime.utcnow():
        st.session_state["authenticated"] = True
        st.session_state["username"] = session_info["username"]
        st.session_state["role"] = session_info["role"]
        st.session_state["user_id"] = session_info["user_id"]
    else:
        st.session_state["authenticated"] = False
