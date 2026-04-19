from __future__ import annotations

import streamlit as st

from components.types import JsonValue


SESSION_DEFAULTS: dict[str, JsonValue] = {
    "page": "home",
    "json_data": None,
    "json_source_format": None,
    "selected_chat_index": None,
    "consent": False,
    "editing_message": None,
    "redacting_message": None,
    "pii": [],
    "deleted_chat_count": 0,
    "deleted_chats": set(),
    "scroll_to_chat_id": False,
    "chat_search_cache": {},
    "chat_date_cache": {},
    "selected_labels": [],
    "show_all": True,
}


def init_session_state() -> None:
    """Seed all session keys used across the multi-page Streamlit flow."""
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_loaded_data() -> None:
    """Clear the currently loaded conversation dataset and derived UI state."""
    st.session_state.json_data = None
    st.session_state.json_source_format = None
    st.session_state.selected_chat_index = None
    st.session_state.redacting_message = None
    st.session_state.pii = []
    st.session_state.deleted_chat_count = 0
    st.session_state.deleted_chats = set()
    st.session_state.chat_search_cache = {}
    st.session_state.chat_date_cache = {}
    st.session_state.selected_labels = []
    st.session_state.show_all = True
