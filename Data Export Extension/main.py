import streamlit as st
from streamlit_scroll_to_top import scroll_to_here
from components.sidebar import render_sidebar
from components.styles import apply_global_style
from components.state import init_session_state
from _pages.home import home_page
from _pages.consent import consent_page
from _pages.upload import upload_page
from _pages.chat_list import chat_list_page
from _pages.chat_details import chat_detail_page
from _pages.instructions import instructions_page

st.set_page_config(
    page_title="AI Conversation Donation",
    layout="wide",
)

init_session_state()

if st.session_state.get("scroll_to_top"):
    if st.session_state.scroll_to_top:
            scroll_to_here(-10, key='top')
            st.session_state.scroll_to_top = False

# --------------------------
# Apply global CSS
# --------------------------
apply_global_style()

# --------------------------
# Render sidebar
# --------------------------
render_sidebar()

# --------------------------
# Page Routing
# --------------------------
page_mapping = {
    "home": home_page,
    "consent": consent_page,
    "upload": upload_page,
    "chat_list": chat_list_page,
    "detail": chat_detail_page,
    "instructions": instructions_page,
}

page_mapping.get(st.session_state.page, home_page)()
