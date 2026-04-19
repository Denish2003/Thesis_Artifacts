import streamlit as st

def go_to_page(page_name):
    """Navigate between app pages and reset scroll position."""
    st.session_state.page = page_name
    st.session_state.scroll_to_top = True
    st.rerun()
