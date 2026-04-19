import streamlit as st
from components.go_to_page import go_to_page
from components.ui import card_grid, inline_notice, page_header, section_intro

def home_page():
    """Landing page for the donation workflow."""
    page_header(
        "AI Conversation Donation Platform",
        "Review, clean, redact, and optionally donate conversation histories in a guided research workflow.",
        eyebrow="Princeton Research Study",
    )

    section_intro(
        "What you can do here",
        "A short guided flow helps you upload data, review sensitive content, and choose whether to export or donate the cleaned result.",
    )
    card_grid(
        [
            {
                "icon": "01",
                "title": "Upload",
                "body": "Import a ChatGPT export or extension-generated JSON file.",
            },
            {
                "icon": "02",
                "title": "Review",
                "body": "Search chats, remove conversations, and redact sensitive text.",
            },
            {
                "icon": "03",
                "title": "Export or Donate",
                "body": "Download a cleaned copy or securely donate it for research.",
            },
        ]
    )

    if "consent" not in st.session_state:
        st.session_state.consent = False

    if st.session_state.consent:
        inline_notice("Consent completed. You can continue to the instructions and upload flow.", tone="success")
        if st.button("Continue to Instructions", width="stretch"):
            go_to_page("instructions")
    else:
        inline_notice(
            "Before continuing, please review the consent form, privacy expectations, and study details.",
            tone="warning",
        )
        if st.button("Review Consent Form", width="stretch"):
            go_to_page("consent")
