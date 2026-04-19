import streamlit as st

def apply_global_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Manrope:wght@400;500;600;700&display=swap');

    :root {
        --app-bg: linear-gradient(180deg, #f6f1e8 0%, #f4f8fb 45%, #eef3f8 100%);
        --panel-bg: rgba(255, 255, 255, 0.82);
        --panel-strong: #ffffff;
        --sidebar-bg: linear-gradient(180deg, #17324d 0%, #204d68 100%);
        --text-main: #17212b;
        --text-soft: #5f6f80;
        --brand: #1e5a7a;
        --brand-strong: #133f58;
        --accent: #d87b4a;
        --border: rgba(23, 33, 43, 0.10);
        --shadow: 0 20px 50px rgba(27, 49, 66, 0.10);
        --radius-lg: 24px;
        --radius-md: 18px;
        --radius-sm: 12px;
    }

    html, body, [class*="css"]  {
        font-family: 'Manrope', sans-serif;
        color: var(--text-main);
    }

    [data-testid="stAppViewContainer"] {
        background: var(--app-bg);
    }

    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    #MainMenu,
    footer {
        display: none;
    }

    [data-testid="stAppViewContainer"] > .main {
        background: transparent;
    }

    .main .block-container {
        padding-top: 0.75rem;
        padding-bottom: 2rem;
        max-width: 1120px;
    }

    h1, h2, h3 {
        font-family: 'Fraunces', serif;
        letter-spacing: -0.03em;
        color: #122033;
    }

    h1 {
        font-size: clamp(2.2rem, 4vw, 3.8rem);
    }

    [data-testid="stSidebar"] {
        background: var(--sidebar-bg);
        color: #eef6fb;
        padding: 1rem;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    [data-testid="stSidebar"] * {
        color: inherit;
    }

    [data-testid="stSidebar"] .stAlert {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.14);
    }

    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.09);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 0.65rem 0.8rem;
    }

    [data-testid="stSidebar"] details {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 16px;
        padding: 0.25rem 0.2rem;
        margin-top: 0.8rem;
    }

    [data-testid="stSidebar"] summary {
        font-weight: 700;
    }

    div.stButton > button,
    div.stDownloadButton > button,
    div[data-testid="stLinkButton"] a {
        background: #d87b4a;
        color: #ffffff;
        border: 0;
        border-radius: 999px;
        font-weight: 700;
        min-height: 2.85rem;
        box-shadow: 0 10px 24px rgba(19, 63, 88, 0.18);
        transition: transform 0.15s ease, box-shadow 0.15s ease, opacity 0.15s ease;
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover,
    div[data-testid="stLinkButton"] a:hover {
        background: #102f43;
        transform: translateY(-1px);
        color: #ffffff;
    }

    div.stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.92);
        color: var(--brand-strong);
        border: 1px solid rgba(19, 63, 88, 0.12);
    }

    div.stButton > button[kind="secondary"]:hover,
    div.stDownloadButton > button[kind="secondary"]:hover {
        background: #ffffff;
        color: var(--brand-strong);
    }

    div.stButton > button[kind="primary"] {
        background: #d87b4a;
        color: #ffffff;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #c86b39;
        color: #ffffff;
    }

    div.stButton > button:disabled,
    div.stDownloadButton > button:disabled {
        background: rgba(255, 255, 255, 0.22) !important;
        color: rgba(255, 255, 255, 0.45) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
        transform: none !important;
        opacity: 1 !important;
    }

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stMultiSelect"] > div,
    [data-testid="stSelectbox"] > div,
    [data-testid="stDateInput"] input {
        background: rgba(255, 255, 255, 0.72);
        border-radius: var(--radius-sm);
        border: 1px solid var(--border);
    }

    [data-testid="stTabs"] {
        background: rgba(255, 255, 255, 0.55);
        padding: 0.35rem;
        border-radius: 999px;
        border: 1px solid rgba(23, 33, 43, 0.08);
        margin-bottom: 1rem;
    }

    [data-testid="stTabs"] button {
        border-radius: 999px;
        font-weight: 700;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        background: #ffffff;
        color: var(--brand-strong);
    }

    [data-testid="stChatMessage"] {
        background: var(--panel-bg);
        border: 1px solid rgba(23, 33, 43, 0.08);
        border-radius: var(--radius-lg);
        padding: 0.85rem 1rem;
        box-shadow: var(--shadow);
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }

    [data-testid="stChatMessageContent"] p {
        line-height: 1.65;
    }

    [data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.78);
        border-radius: var(--radius-md);
    }

    .ddp-hero-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.86) 0%, rgba(246,250,253,0.88) 100%);
        border: 1px solid rgba(23, 33, 43, 0.08);
        border-radius: 28px;
        box-shadow: var(--shadow);
        padding: 1.4rem 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(12px);
    }

    .ddp-page-hero {
        padding: 0.05rem 0 0.7rem;
    }

    .ddp-page-eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.8rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .ddp-page-subtitle {
        color: var(--text-soft);
        font-size: 1.04rem;
        max-width: 760px;
        margin-top: 0.35rem;
        line-height: 1.7;
    }

    .ddp-subtle {
        color: var(--text-soft);
        font-size: 0.98rem;
    }

    .ddp-section-intro {
        margin: 0.75rem 0 0.6rem;
    }

    .ddp-section-intro p {
        color: var(--text-soft);
        max-width: 760px;
        line-height: 1.7;
        margin: 0.15rem 0 0;
    }

    .ddp-info-card {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(23, 33, 43, 0.08);
        border-radius: 22px;
        padding: 1rem;
        box-shadow: var(--shadow);
        min-height: 0;
    }

    .ddp-info-card h3 {
        margin: 0rem 0rem;
        font-size: 1.05rem;
    }

    .ddp-info-card p {
        color: var(--text-soft);
        line-height: 1.5;
        margin-bottom: 0;
        font-size: 0.95rem;
    }

    .ddp-card-icon {
        font-size: 1.35rem;
    }

    .ddp-kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.8rem;
        margin: 1rem 0 0.25rem;
    }

    .ddp-kpi {
        background: rgba(255, 255, 255, 0.75);
        border: 1px solid rgba(23, 33, 43, 0.08);
        border-radius: 18px;
        padding: 0.9rem 1rem;
    }

    .ddp-kpi-label {
        color: var(--text-soft);
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
    }

    .ddp-kpi-value {
        color: var(--brand-strong);
        font-size: 1.35rem;
        font-weight: 800;
        margin-top: 0.2rem;
    }

    .ddp-step-card {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(23, 33, 43, 0.08);
        border-radius: 24px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
    }

    .ddp-step-media {
        border-radius: 20px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(23, 33, 43, 0.08);
        box-shadow: 0 12px 28px rgba(27, 49, 66, 0.08);
    }

    .ddp-step-media [data-testid="stImage"] {
        width: 100%;
    }

    .ddp-step-media img {
        width: 100%;
        height: 240px;
        object-fit: cover;
        display: block;
    }

    .ddp-step-copy p {
        color: var(--text-soft);
        line-height: 1.7;
        margin-bottom: 0;
    }

    .ddp-step-pill {
        display: inline-block;
        background: rgba(30, 90, 122, 0.10);
        color: var(--brand-strong);
        border-radius: 999px;
        padding: 0.25rem 0.7rem;
        font-size: 0.8rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.4rem;
    }

    .ddp-chat-row-card {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(23, 33, 43, 0.08);
        border-radius: 20px;
        padding: 1rem 1.05rem;
        box-shadow: 0 10px 24px rgba(27, 49, 66, 0.06);
    }

    .ddp-chat-title {
        font-weight: 800;
        color: #132236;
        margin-bottom: 0.2rem;
    }

    .ddp-chat-title-deleted {
        text-decoration: line-through;
        color: var(--text-soft);
    }

    .ddp-chat-meta {
        color: var(--text-soft);
        font-size: 0.9rem;
        margin-bottom: 0.45rem;
    }

    .ddp-chat-body {
        color: #314050;
        line-height: 1.55;
        margin: 0;
    }

    .ddp-message-meta {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.55rem;
        flex-wrap: wrap;
    }

    .ddp-role-badge {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 0.2rem 0.72rem;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .ddp-role-user {
        background: rgba(30, 90, 122, 0.10);
        color: var(--brand-strong);
    }

    .ddp-role-assistant {
        background: rgba(216, 123, 74, 0.14);
        color: #8a4c29;
    }

    .ddp-meta-chip {
        background: rgba(19, 63, 88, 0.06);
        color: var(--text-soft);
        border-radius: 999px;
        padding: 0.2rem 0.65rem;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .ddp-inline-note {
        background: rgba(216, 123, 74, 0.08);
        border: 1px solid rgba(216, 123, 74, 0.20);
        color: #7d4a31;
        border-radius: 16px;
        padding: 0.85rem 1rem;
        margin-bottom: 1rem;
    }

    .ddp-inline-note-success {
        background: rgba(73, 153, 114, 0.10);
        border-color: rgba(73, 153, 114, 0.20);
        color: #2f6f52;
    }

    .ddp-inline-note-warning {
        background: rgba(209, 144, 34, 0.10);
        border-color: rgba(209, 144, 34, 0.20);
        color: #7b5a10;
    }

    .ddp-list {
        color: var(--text-main);
        line-height: 1.75;
    }

    .ddp-list li {
        margin-bottom: 0.4rem;
    }

    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 0.5rem;
        }

        [data-testid="stChatMessage"] {
            border-radius: 18px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
