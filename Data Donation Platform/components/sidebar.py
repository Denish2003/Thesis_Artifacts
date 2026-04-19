from components.state import reset_loaded_data
import streamlit as st
import json
from components.save_data_to_VM import save_donation
from _pages.consent import consent_page
from _pages.instructions import instructions_page
from components.go_to_page import go_to_page
from components.ui import inline_notice

SURVEY_URL = "https://princetonsurvey.az1.qualtrics.com/jfe/form/SV_6n6ZLEs8M8fYBoy"

# ------------------ Dialogs ------------------ #
@st.dialog("Survey", dismissible=True)
def survey_modal(url):
    st.write(
        "Thank you for donating your data. Please complete the survey so the research team can send your gift card."
    )
    st.link_button("Take Survey", url, width='stretch')

@st.dialog("Consent Form", dismissible=True, width="medium")
def consent_modal():
    consent_page(isModal=True)

@st.dialog("Instructions", dismissible=True, width="medium")
def instructions_modal():
    instructions_page(isModal=True)

# ------------------ Sidebar ------------------ #
def render_sidebar():
    """Render navigation and export tools for the active workflow pages."""
    if st.session_state.page not in ["home", "consent"]:
        with st.sidebar:
            st.title("AI Conversation Review")
            st.caption("Clean, export, or donate reviewed conversations.")

            nav_col1, nav_col2 = st.columns(2)
            with nav_col1:
                if st.button("Home", width="stretch", type="secondary"):
                    go_to_page("home")
            with nav_col2:
                if st.button("Upload", width="stretch", type="secondary"):
                    reset_loaded_data()
                    go_to_page("upload")

            nav_col3, nav_col4 = st.columns(2)
            with nav_col3:
                if st.button("Instructions", width="stretch", type="secondary"):
                    instructions_modal()
            with nav_col4:
                if st.button("Consent", width="stretch", type="secondary"):
                    consent_modal()

            json_data = st.session_state.get("json_data", [])
            if json_data:
                cleaned_data = [
                    chat for idx, chat in enumerate(json_data)
                    if idx not in st.session_state.deleted_chats
                ]
                source_format = st.session_state.get("json_source_format", "chatgpt_export")
                export_payload = (
                    {"conversations": cleaned_data}
                    if source_format == "extension_export"
                    else cleaned_data
                )
                final_json_str = json.dumps(export_payload, indent=2)

                st.subheader("Ready to Export")
                st.download_button(
                    label="Download Cleaned JSON",
                    data=final_json_str,
                    file_name="cleaned_conversations.json",
                    mime="application/json",
                    width="stretch",
                    type="secondary",
                )

                st.markdown("###### Donate for Research")
                consent = st.checkbox(
                    "I understand the cleaned data will be stored for research purposes."
                )
                donate_clicked = st.button(
                    "Donate Data",
                    disabled=not consent,
                    width="stretch",
                    type="primary",
                )
                if donate_clicked:
                    save_donation(export_payload)
                    inline_notice("Your cleaned data was securely stored on the research server.", tone="success")
                    survey_modal(SURVEY_URL)
            else:
                st.subheader("Get Started")
                st.info("No chats loaded yet.")
                if st.button("Upload a File", width="stretch", type="primary"):
                    go_to_page("upload")
