from __future__ import annotations

import re

import streamlit as st
from components.save_data_to_VM import save_email

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    """Perform lightweight email validation for reminder signups."""
    return bool(EMAIL_PATTERN.match(email.strip()))


def send_reminder(email: str) -> None:
    """Persist a reminder email and refresh the dialog state."""
    save_email(email)
    st.session_state.reminder_saved = True
    st.rerun()

@st.dialog("ChatGPT Export Reminder")
def reminder_modal():
    """Collect reminder email addresses for users waiting on the export."""
    if "reminder_saved" not in st.session_state:
        st.session_state.reminder_saved = False

    st.write(
        """
        OpenAI can take **3–4 days** to provide your ChatGPT data after you request it.

        Enter your email below, and we'll remind you **to come back and upload or donate your data** once it’s likely ready.
        """
    )

    email = st.text_input("Email address", key="reminder_email").strip()
    if st.session_state.get("reminder_saved"):
        st.success("Reminder saved. You can close this dialog.")
    elif email and not is_valid_email(email):
        st.warning("Enter a valid email address to receive a reminder.")

    st.button(
        "Send me a reminder",
        key="reminder_button",
        disabled=not email or not is_valid_email(email),
        on_click=send_reminder,
        args=(email,),
        width='stretch',
    )
