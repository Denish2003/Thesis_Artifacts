from __future__ import annotations

import streamlit as st
from datetime import datetime
from components.go_to_page import go_to_page
from components.chat_schema import extract_chat_text, get_chat_datetime
from components.state import reset_loaded_data
from components.ui import chat_list_item, inline_notice, page_header, stat_row
from components.types import ChatRecord


def get_chat_preview(chat: ChatRecord) -> str:
    """Build a short text preview for the chat list cards."""
    preview = extract_chat_text(chat).replace("\n", " ").strip()
    if len(preview) > 180:
        return f"{preview[:177]}..."
    return preview


def chat_list_page() -> None:
    """Search, filter, and manage the uploaded conversations."""
    if st.button("⬅ Back to Upload"):
        reset_loaded_data()
        go_to_page("upload")

    all_chats = st.session_state.get("json_data")
    if not all_chats:
        st.info("No chats loaded.")
        return

    page_header(
        "Chat History",
        "Browse uploaded conversations, filter by month, search by title or content, and remove anything you do not want included.",
        eyebrow="Review",
    )

    months = set()

    for idx, chat in enumerate(all_chats):
        # Cache expensive derived values once per loaded dataset so filtering stays
        # responsive even when the page reruns after every button click.
        if idx not in st.session_state.chat_date_cache:
            st.session_state.chat_date_cache[idx] = get_chat_datetime(chat)

        dt = st.session_state.chat_date_cache[idx]
        if dt:
            months.add((dt.year, dt.month))

        if idx not in st.session_state.chat_search_cache:
            st.session_state.chat_search_cache[idx] = extract_chat_text(chat).lower()

    stat_row(
        [
            {"label": "Loaded Conversations", "value": len(all_chats)},
            {"label": "Excluded", "value": len(st.session_state.deleted_chats)},
            {"label": "Included", "value": len(all_chats) - len(st.session_state.deleted_chats)},
        ]
    )
    inline_notice(
        "Delete removes a conversation from the cleaned export only. You can undo it at any time before donation or download.",
        tone="info",
    )

    sorted_months = sorted(months, reverse=True)

    show_all = st.toggle(
        "Show all chats",
        value=st.session_state.show_all,
        key="show_all_widget",
    )

    st.session_state.show_all = show_all

    selected_months_set = set()

    if not st.session_state.show_all and sorted_months:
        options = [
            f"{datetime(year=y, month=m, day=1).strftime('%B %Y')}"
            for y, m in sorted_months
        ]

        latest_year, latest_month = sorted_months[0]

        default_label = datetime(
            year=latest_year,
            month=latest_month,
            day=1
        ).strftime("%B %Y")

        if "selected_labels" not in st.session_state:
            st.session_state.selected_labels = [default_label]

        st.session_state.selected_labels = [
            label for label in st.session_state.selected_labels
            if label in options
        ]

        selected_labels = st.multiselect(
            "Filter by Month(s)",
            options,
            default=st.session_state.selected_labels,
            key="selected_labels_widget"
        )

        if selected_labels:
            st.session_state.selected_labels = selected_labels

        # Convert the human-readable month labels back into `(year, month)` tuples
        # for fast comparisons during the filtering loop below.
        for label in st.session_state.selected_labels:
            if label in options:
                idx_option = options.index(label)
                selected_months_set.add(sorted_months[idx_option])

    search_query = st.text_input(
        "Search chats (title or content)",
        placeholder="Type to filter chats...",
    ).lower().strip()

    filtered_chats = []

    for idx, chat in enumerate(all_chats):
        title = chat.get("title", "Conversation")
        chat_text = st.session_state.chat_search_cache[idx]
        dt = st.session_state.chat_date_cache[idx]

        # Apply month filters before text search so we short-circuit early.
        if not show_all:
            if not selected_months_set:
                continue
            if dt and (dt.year, dt.month) not in selected_months_set:
                continue

        if (
            not search_query
            or search_query in title.lower()
            or search_query in chat_text
        ):
            filtered_chats.append((idx, chat))

    if not filtered_chats:
        st.info("No chats match your filters.")
        return

    for original_index, chat in filtered_chats:
        title = chat.get("title", "Conversation")
        dt = st.session_state.chat_date_cache[original_index]
        date_label = dt.strftime("%b %d, %Y") if dt else "Unknown date"
        is_deleted = original_index in st.session_state.deleted_chats
        preview = get_chat_preview(chat)

        col1, col2, col3 = st.columns([6, 1.2, 1.2])
        with col1:
            chat_list_item(title, date_label, preview, deleted=is_deleted)

        with col2:
            if st.button("Open →", key=f"open_chat_{original_index}"):
                st.session_state.selected_chat_index = original_index
                go_to_page("detail")

        with col3:
            if not is_deleted:
                if st.button("Delete", key=f"delete_chat_{original_index}"):
                    st.session_state.deleted_chats.add(original_index)
                    st.session_state.deleted_chat_count += 1
                    st.rerun()
            else:
                if st.button("Undo", key=f"undo_delete_{original_index}"):
                    st.session_state.deleted_chats.remove(original_index)
                    st.session_state.deleted_chat_count = max(
                        st.session_state.deleted_chat_count - 1,
                        0,
                    )
                    st.rerun()
