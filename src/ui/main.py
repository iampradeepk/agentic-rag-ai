"""
Streamlit main entrypoint for LLMinate RAG AI UI.
Renders navigation for Chat, Admin, and Agent Dashboard.
"""
import streamlit as st
from src.ui.chat_app import ChatInterface
from src.ui.admin_app import AdminInterface

st.set_page_config(page_title="LLMinate RAG AI", layout="wide")

from src.ui.auth_ui import AuthUI
from src.ui.agent_dashboard import AgentDashboardInterface

PAGES = {
    "Login": AuthUI,
    "Chat": ChatInterface,
    "Admin": AdminInterface,
    "Agent Dashboard": AgentDashboardInterface,
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page_class = PAGES[selection]
page = page_class()

if selection == "Login":
    page.render_auth_interface()
elif selection == "Chat":
    page.render_chat_interface()
elif selection == "Admin":
    page.render_admin_interface()
elif selection == "Agent Dashboard":
    page.render_dashboard_interface()
