from __future__ import annotations

import streamlit as st
import pandas as pd
from components.PII import pii
import difflib
from html import escape
from components.go_to_page import go_to_page
from components.chat_schema import get_chat_messages, update_message_text
from components.types import ChatRecord, NormalizedMessage, PiiMatch

# --- Helper functions ---
def highlight_pii(text: str, pii_data: list[PiiMatch]) -> str:
    """Wrap detected entities in inline markup so they stand out during review."""
    if not pii_data or not text:
        return text
    highlighted = text
    for p in sorted(pii_data, key=lambda x: -len(x["Text"])):
        highlighted = highlighted.replace(
            p["Text"],
            f"<span style='background-color:#ffe6e6; color:#990000; font-weight:bold;'>{p['Text']}</span>"
        )
    return highlighted

def redact_all_text(text: str) -> str:
    """Replace the full message with a compact placeholder showing redacted length."""
    length = len(text)
    return f"{{Redacted {length} chars}}" if length >= 50 else "{Redacted <50 chars}"

def selective_redact_delete_only(original_text: str, edited_text: str) -> str:
    """Allow deletions only and convert removed spans into standard redaction markers."""
    result = []
    s = difflib.SequenceMatcher(None, original_text, edited_text)
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == "equal":
            result.append(original_text[i1:i2])
        elif tag in ("delete", "replace"):
            length = i2 - i1
            if length < 50:
                result.append(" {Redacted <50 chars} ")
            else:
                result.append(f"{{Redacted {length} chars}}")
        elif tag == "insert":
            continue
    return "".join(result)

def remove_redacted_pii(text: str) -> bool:
    """Skip highlighting logic for placeholder-only redacted messages."""
    return text.startswith("{Redacted")

def format_role_label(role: str) -> str:
    return {
        "assistant": "Assistant",
        "user": "User",
    }.get(role, role.capitalize())

def render_chat_header(data: ChatRecord, messages: list[NormalizedMessage]) -> None:
    """Show conversation-level summary metadata above the detailed review tabs."""
    date_label = escape(str(data.get("savedAt", "Unknown date")))
    chat_url = data.get("url")
    pii_count = sum(len(m["pii"]) for m in messages if m["pii"] and not remove_redacted_pii(m["text"]))
    title = escape(str(data.get("title", "Conversation")))

    st.markdown(
        f"""
        <div class="ddp-hero-card">
            <div class="ddp-subtle">Conversation review</div>
            <h1 style="margin:0.25rem 0 0.45rem;">{title}</h1>
            <div class="ddp-subtle">Review message content, redact sensitive text, and export a cleaned version when you're ready.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_message_meta(message: NormalizedMessage) -> None:
    """Render role, timestamp, and PII counts in a compact header row."""
    role_label = escape(format_role_label(message["role"]))
    role_class = "ddp-role-assistant" if message["role"] == "assistant" else "ddp-role-user"
    meta_bits: list[str] = []
    if message["time"]:
        meta_bits.append(str(message["time"]))
    if message["pii"] and not remove_redacted_pii(message["text"]):
        meta_bits.append(f"{len(message['pii'])} PII flag(s)")

    col1, col2 = st.columns([1.5, 4], vertical_alignment="center")
    with col1:
        st.markdown(
            f'<div class="ddp-message-meta"><span class="ddp-role-badge {role_class}">{role_label}</span></div>',
            unsafe_allow_html=True,
        )
    with col2:
        if meta_bits:
            st.caption(" • ".join(meta_bits))

def collect_message_pii(messages: list[NormalizedMessage]) -> list[PiiMatch]:
    """Build a deduplicated list of PII matches for the review table."""
    unique_pii: list[PiiMatch] = []
    seen_texts: set[str] = set()
    for message in messages:
        if message["pii"] and not remove_redacted_pii(message["text"]):
            for pii_match in message["pii"]:
                pii_text = pii_match.get("Text")
                if pii_text and pii_text not in seen_texts:
                    unique_pii.append(pii_match)
                    seen_texts.add(pii_text)
    return unique_pii


def chat_detail_page() -> None:
    data = st.session_state.json_data[st.session_state.selected_chat_index]

    if st.button("⬅ Back to Chat List"):
        st.session_state.page = "chat_list"
        st.rerun()

    messages: list[NormalizedMessage] = []
    for message in get_chat_messages(data):
        # PII is computed from the normalized message text so the same review UI works
        # for both legacy ChatGPT exports and the extension message format.
        pii_result = pii(message["text"])
        if pii_result:
            if "pii" not in st.session_state:
                st.session_state.pii = []
            st.session_state.pii.append(pii_result)

        message["pii"] = pii_result
        messages.append(message)

    render_chat_header(data, messages)

    tab1, tab2 = st.tabs(["Conversation", "Detected PII"])

    # --- Conversation Tab ---
    with tab1:
        st.markdown(
            """
            <div class="ddp-inline-note">
                Use <strong>Redact</strong> to hide only the selected parts of a message, or <strong>Redact All</strong> to replace the whole message with a placeholder.
            </div>
            """,
            unsafe_allow_html=True,
        )
        for m in messages:
            with st.chat_message(m["role"]):
                render_message_meta(m)

                # Redacted placeholders should render as-is. Otherwise, show inline
                # highlights when PII was detected for that message.
                if remove_redacted_pii(m["text"]):
                    st.markdown(m["text"], unsafe_allow_html=True)
                elif m["pii"]:
                    highlighted = highlight_pii(m["text"], m["pii"])
                    st.markdown(highlighted, unsafe_allow_html=True)
                else:
                    st.markdown(m["text"], unsafe_allow_html=True)

                # Redact / Redact All buttons
                if not remove_redacted_pii(m["text"]):
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Redact", key=f"redact_{m['id']}"):
                            st.session_state.redacting_message = m["id"]
                            st.rerun()
                    with col2:
                        # Avoid showing a conflicting full-message action while a
                        # selective edit box is open for another message.
                        if st.session_state.get("redacting_message") is None:
                            if st.button("Redact All", key=f"redactall_{m['id']}"):
                                new_text = redact_all_text(m["text"])
                                update_message_text(data, m, new_text)
                                st.session_state.json_data[st.session_state.selected_chat_index] = data
                                st.rerun()

            # The editor intentionally treats any replacement as a deletion so users
            # can only hide content, not add or rewrite message text.
            if st.session_state.get("redacting_message") == m["id"]:
                edited_text = st.text_area(
                    "Delete text you want hidden (cannot add new characters):",
                    value=m["text"],
                    key=f"edit_redact_{m['id']}"
                )
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save Redaction", key=f"save_redact_{m['id']}"):
                        new_text = selective_redact_delete_only(m["text"], edited_text)
                        update_message_text(data, m, new_text)
                        st.session_state.json_data[st.session_state.selected_chat_index] = data
                        st.session_state.redacting_message = None
                        st.success("Message redacted.")
                        st.rerun()
                with col2:
                    if st.button("Cancel", key=f"cancel_redact_{m['id']}"):
                        st.session_state.redacting_message = None
                        st.rerun()

    with tab2:
        st.subheader("Detected PII Information")
        unique_pii = collect_message_pii(messages)
        if unique_pii:
            pii_df = pd.DataFrame(unique_pii)
            st.dataframe(pii_df, width='stretch')
        else:
            st.info("No PII detected in this conversation.")
