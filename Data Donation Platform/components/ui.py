from __future__ import annotations

from html import escape
from typing import Sequence

import streamlit as st

from components.types import StatItem, StepItem


def page_header(title: str, subtitle: str | None = None, eyebrow: str | None = None) -> None:
    """Render a consistent page hero across the app."""
    eyebrow_html = (
        f'<div class="ddp-subtle ddp-page-eyebrow">{escape(eyebrow)}</div>'
        if eyebrow
        else ""
    )
    subtitle_html = (
        f'<p class="ddp-page-subtitle">{escape(subtitle)}</p>'
        if subtitle
        else ""
    )
    st.markdown(
        f"""
        <section class="ddp-page-hero">
            {eyebrow_html}
            <h1>{escape(title)}</h1>
            {subtitle_html}
        </section>
        """,
        unsafe_allow_html=True,
    )


def card_grid(items: Sequence[StepItem], columns: int = 3) -> None:
    """Render a responsive set of content cards using Streamlit columns."""
    cols = st.columns(columns)
    for index, item in enumerate(items):
        with cols[index % columns]:
            title = escape(item["title"])
            body = escape(item["body"])
            st.markdown(
                f"""
                <div class="ddp-info-card">
                    <h3>{title}</h3>
                    <p>{body}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div style='margin-top: 20px'></div>", unsafe_allow_html=True)



def stat_row(items: Sequence[StatItem]) -> None:
    """Render compact summary stats."""
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        with col:
            st.markdown(
                f"""
                <div class="ddp-kpi">
                    <div class="ddp-kpi-label">{escape(item["label"])}</div>
                    <div class="ddp-kpi-value">{escape(str(item["value"]))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div style='margin-top: 20px'></div>", unsafe_allow_html=True)



def section_intro(title: str, body: str) -> None:
    """Render a section heading followed by muted copy."""
    st.markdown(
        f"""
        <div class="ddp-section-intro">
            <h3>{escape(title)}</h3>
            <p>{escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def step_card(
    step_number: int,
    title: str,
    description: str,
    image_path: str | None = None,
    extra_html: str = "",
) -> None:
    """Render a single procedural step with optional media."""
    col1, col2 = st.columns([1.3, 1], vertical_alignment="center")
    with col1:
        st.markdown(
            f"""
            <div class="ddp-step-card">
                <div class="ddp-step-pill">Step {step_number}</div>
                <h3>{escape(title)}</h3>
                <p>{escape(description)}</p>
                {extra_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        if image_path:
            st.markdown('<div class="ddp-step-media">', unsafe_allow_html=True)
            st.image(image_path, width='stretch')
            st.markdown("</div>", unsafe_allow_html=True)


def chat_list_item(title: str, subtitle: str, body: str, deleted: bool = False) -> None:
    """Render a clean chat list summary row."""
    title_class = "ddp-chat-title ddp-chat-title-deleted" if deleted else "ddp-chat-title"
    body_html = f'<p class="ddp-chat-body">{escape(body)}</p>' if body else ""
    st.markdown(
        f"""
        <div class="ddp-chat-row-card">
            <div class="{title_class}">{escape(title)}</div>
            <div class="ddp-chat-meta">{escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='margin-top: 10px'></div>", unsafe_allow_html=True)


def inline_notice(body: str, tone: str = "info") -> None:
    """Render a styled inline callout."""
    tone_class = {
        "info": "ddp-inline-note",
        "success": "ddp-inline-note ddp-inline-note-success",
        "warning": "ddp-inline-note ddp-inline-note-warning",
    }.get(tone, "ddp-inline-note")
    st.markdown(
        f'<div class="{tone_class}">{escape(body)}</div>',
        unsafe_allow_html=True,
    )
