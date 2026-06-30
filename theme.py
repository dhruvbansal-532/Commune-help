"""
theme.py — Commune Help design system for Streamlit
Drop this in your project and call inject_theme() once at the top of app.py,
right after st.set_page_config().
"""

import streamlit as st
import textwrap


def inject_theme():
    css = textwrap.dedent("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
        :root{
            --primary:#2563EB; --primary-dark:#1d4ed8;
            --secondary:#10B981;
            --accent:#F59E0B;
            --error:#EF4444;
            --bg:#F8FAFC; --card:#FFFFFF; --border:#E5E7EB;
            --text:#1E293B; --text-soft:#64748B;
            --radius:18px;
            --shadow: 0 2px 8px rgba(30,41,59,0.04), 0 8px 24px rgba(30,41,59,0.06);
            --shadow-hover: 0 4px 14px rgba(30,41,59,0.06), 0 14px 32px rgba(30,41,59,0.10);
        }

        html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
        h1, h2, h3 { font-family: 'Manrope', sans-serif !important; font-weight: 800 !important; letter-spacing: -0.02em; color: var(--text); }

        .stApp {
            background: var(--bg);
            background-image:
              radial-gradient(circle at 10% 5%, rgba(37,99,235,0.05), transparent 40%),
              radial-gradient(circle at 90% 15%, rgba(16,185,129,0.05), transparent 40%);
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: rgba(255,255,255,0.7);
            backdrop-filter: blur(12px);
            border-right: 1px solid var(--border);
        }

        /* Card container - wrap any st.container(border=True) content in this look */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: var(--radius) !important;
            border: 1px solid var(--border) !important;
            box-shadow: var(--shadow);
            background: var(--card);
            transition: box-shadow .25s, transform .25s;
            padding: 4px;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            box-shadow: var(--shadow-hover);
            transform: translateY(-2px);
        }

        /* Buttons */
        .stButton > button {
            background: var(--primary);
            color: #fff;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            font-size: 14px;
            padding: 0.55rem 1.4rem;
            box-shadow: 0 4px 12px rgba(37,99,235,0.25);
            transition: all .2s ease;
        }
        .stButton > button:hover {
            background: var(--primary-dark);
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(37,99,235,0.32);
        }
        .stButton > button:focus-visible {
            outline: 3px solid #93C5FD;
            outline-offset: 2px;
        }

        /* Secondary / ghost buttons -> apply via use_container_width + custom class trick,
           or simplest: wrap secondary actions with st.button(..., type="secondary") */
        .stButton > button[kind="secondary"] {
            background: #fff;
            color: var(--primary);
            border: 1.5px solid var(--primary);
            box-shadow: none;
        }
        .stButton > button[kind="secondary"]:hover {
            background: #EFF6FF;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid var(--border); }
        .stTabs [data-baseweb="tab"] {
            font-weight: 600; font-size: 14px; color: var(--text-soft);
            padding: 11px 18px;
        }
        .stTabs [aria-selected="true"] {
            color: var(--primary) !important;
            border-bottom: 2.5px solid var(--primary) !important;
        }

        /* Inputs */
        .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            border-radius: 10px !important;
            border: 1px solid var(--border) !important;
            background: #F8FAFC !important;
            font-weight: 600 !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(37,99,235,0.15) !important;
        }

        /* File uploader */
        [data-testid="stFileUploaderDropzone"] {
            border: 2px dashed #CBD5E1 !important;
            border-radius: 14px !important;
            background: #F8FAFC !important;
            transition: all .25s;
        }
        [data-testid="stFileUploaderDropzone"]:hover {
            border-color: var(--primary) !important;
            background: #EFF6FF !important;
        }

        /* Checkbox */
        .stCheckbox label p { font-weight: 600; font-size: 13.5px; }

        /* Status badges - use st.markdown with these classes */
        .badge { display:inline-flex; align-items:center; gap:6px; font-size:12px; font-weight:700; padding:5px 11px; border-radius:20px; }
        .badge-low { background:#ECFDF5; color:#047857; }
        .badge-medium { background:#FFFBEB; color:#B45309; }
        .badge-high { background:#FEF2F2; color:#B91C1C; }
        .badge-resolved { background:#ECFDF5; color:#047857; }
        .badge-pending { background:#FFFBEB; color:#B45309; }
        .badge-in-progress { background:#EFF6FF; color:#1D4ED8; }
        .badge-urgent { background:#FEF2F2; color:#B91C1C; }
        .badge-rejected { background:#F1F5F9; color:#475569; }

        /* Stepper - use st.markdown with this snippet, see components.py */
        .step-dot { width:30px;height:30px;border-radius:50%;color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700; }
        .step-dot.done { background:var(--secondary); }
        .step-dot.active { background:var(--primary); box-shadow:0 0 0 4px rgba(37,99,235,0.12); }
        .step-dot.todo { background:#E2E8F0; color:var(--text-soft); }

        /* Hide default Streamlit chrome for a cleaner look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """)
    # Streamlit's markdown parser treats blank lines as paragraph breaks, which can
    # split a <style> block apart and cause raw CSS to render as plain text. Strip
    # blank lines to keep it as one continuous HTML/CSS block.
    css = "\n".join(line for line in css.split("\n") if line.strip() != "")
    st.markdown(css, unsafe_allow_html=True)


def badge(text: str, kind: str = "medium", icon: str = "⚠") -> str:
    """Returns HTML for a status/severity badge. Use with st.markdown(badge(...), unsafe_allow_html=True)."""
    return f'<span class="badge badge-{kind}">{icon} {text}</span>'


def stepper(current_step: int, labels: list[str]) -> str:
    """Returns HTML for a 3-step progress indicator."""
    parts = []
    for i, label in enumerate(labels, start=1):
        if i < current_step:
            parts.append(f'<div class="step-dot done">✓</div><span style="font-size:13px;font-weight:600;margin-right:18px;">{label}</span>')
        elif i == current_step:
            parts.append(f'<div class="step-dot active">{i}</div><span style="font-size:13px;font-weight:600;margin-right:18px;">{label}</span>')
        else:
            parts.append(f'<div class="step-dot todo">{i}</div><span style="font-size:13px;color:#64748B;margin-right:18px;">{label}</span>')
    return f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:24px;">{"".join(parts)}</div>'
