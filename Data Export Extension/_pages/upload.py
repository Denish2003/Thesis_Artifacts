from __future__ import annotations

import streamlit as st
import json
import zipfile
import io
from components.go_to_page import go_to_page
from components.chat_schema import normalize_conversation_payload
from components.ui import inline_notice, page_header
from components.state import reset_loaded_data
from components.types import JsonValue


def parse_uploaded_payload(uploaded_file: st.runtime.uploaded_file_manager.UploadedFile) -> JsonValue:
    """Decode either a raw JSON upload or a ZIP containing `conversations.json`."""
    file_bytes = uploaded_file.read()

    if uploaded_file.type == "application/zip":
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
            json_file_name = next(
                (name for name in z.namelist() if name.endswith("conversations.json")),
                None,
            )
            if not json_file_name:
                raise ValueError("Could not find conversations.json in ZIP.")

            with z.open(json_file_name) as f:
                return json.load(f)

    return json.loads(file_bytes)


def upload_page() -> None:
    """Upload page for ChatGPT and extension JSON payloads."""
    if st.button("⬅ Back to Instructions"):
        go_to_page("instructions")

    if st.session_state.get("json_data"):
        go_to_page("chat_list")
        return

    page_header(
        "Upload Conversation Data",
        "Upload a JSON export from ChatGPT or a JSON file produced by your browser extension. ZIP uploads containing conversations.json are also supported.",
        eyebrow="Upload",
    )
    inline_notice(
        "The file is processed in your current session so you can review and redact it before taking any export or donation action.",
        tone="info",
    )

    uploaded_file = st.file_uploader(
        "Choose a JSON or ZIP file",
        type=["json", "zip"],
    )

    if uploaded_file is None:
        return

    try:
        data = parse_uploaded_payload(uploaded_file)

        conversations, source_format = normalize_conversation_payload(data)

        # Reset any derived state from a previous upload before storing the new dataset.
        reset_loaded_data()
        st.session_state.json_data = conversations
        st.session_state.json_source_format = source_format
        go_to_page("chat_list")

    except zipfile.BadZipFile:
        st.error("Invalid ZIP file.")
    except json.JSONDecodeError:
        st.error("Could not read JSON file.")
    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
