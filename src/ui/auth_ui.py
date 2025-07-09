"""
Streamlit Auth UI for JWT login (stub/initial implementation).
"""
import streamlit as st
import jwt
import datetime

SECRET_KEY = "changeme"  # In production, use a secure env var

class AuthUI:
    def __init__(self):
        self.token = None

    def render_auth_interface(self):
        st.title("Login to LLMinate RAG AI")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if self._authenticate(username, password):
                self.token = self._generate_jwt(username)
                st.session_state["jwt_token"] = self.token
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")
        if "jwt_token" in st.session_state:
            st.info(f"JWT: {st.session_state['jwt_token']}")

    def _authenticate(self, username, password):
        # TODO: Replace with real user DB/auth
        return username == "admin" and password == "admin"

    def _generate_jwt(self, username):
        payload = {
            "sub": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
