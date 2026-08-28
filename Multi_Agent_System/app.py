"""Professional web interface for the Multi-Agent System."""

from __future__ import annotations

import html
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st


ROOT = Path(__file__).resolve().parent
DOCUMENTS_DIR = ROOT / "data" / "documents"

st.set_page_config(
    page_title="Meta Factory",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

        :root {
            --ink:#f5f7fb;
            --muted:#8e9aad;
            --line:#263043;
            --panel:#121a28;
            --panel2:#172133;
            --accent:#8b7cff;
            --cyan:#45d6c8;
        }

        .stApp {
            background:#0b111d;
            color:var(--ink);
            font-family:'Manrope', sans-serif;
        }

        [data-testid="stHeader"] {
            background:transparent;
        }

        [data-testid="stSidebar"] {
            background:#0d1422;
            border-right:1px solid var(--line);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding:1.6rem 1.2rem;
        }

        .brand {
            display:flex;
            align-items:center;
            gap:.7rem;
            margin-bottom:2.2rem;
        }

        .brand-mark {
            width:34px;
            height:34px;
            border-radius:10px;
            display:grid;
            place-items:center;
            background:linear-gradient(135deg,#9e90ff,#5749cc);
            box-shadow:0 8px 26px #6859e540;
            font-size:19px;
        }

        .brand-name {
            font-size:17px;
            font-weight:800;
            letter-spacing:-.04em;
        }

        .brand-sub {
            color:#738098;
            font-size:10px;
            margin-top:2px;
            letter-spacing:.08em;
            text-transform:uppercase;
        }

        .side-label {
            color:#66748b;
            font-size:10px;
            font-weight:700;
            text-transform:uppercase;
            letter-spacing:.13em;
            margin:1.7rem 0 .65rem;
        }

        .side-item {
            padding:.62rem .7rem;
            color:#aab4c5;
            border-radius:8px;
            margin:.18rem 0;
            font-size:13px;
        }

        .side-item.active {
            background:#1d2740;
            color:#fff;
            box-shadow:inset 3px 0 #8b7cff;
        }

        .project-dot {
            display:inline-block;
            width:7px;
            height:7px;
            border-radius:50%;
            margin-right:9px;
            background:#45d6c8;
        }

        .project-dot.blue {
            background:#5f9dff;
        }

        .project-dot.orange {
            background:#f5ae5c;
        }

        .user-card {
            border:1px solid var(--line);
            background:#111a2a;
            border-radius:11px;
            padding:.75rem;
            display:flex;
            gap:.6rem;
            align-items:center;
            margin-top:2rem;
        }

        .avatar {
            display:grid;
            place-items:center;
            width:28px;
            height:28px;
            border-radius:50%;
            background:#d5ceff;
            color:#322b78;
            font-weight:800;
            font-size:11px;
        }

        .user-name {
            font-size:12px;
            font-weight:700;
        }

        .user-role {
            color:#718098;
            font-size:10px;
        }

        .main-wrap {
            max-width:1120px;
            margin:0 auto;
            padding:1.8rem 2.8rem 4rem;
        }

        .topbar {
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:2.8rem;
        }

        .eyebrow {
            color:#8793a8;
            font-size:11px;
            letter-spacing:.15em;
            text-transform:uppercase;
            font-family:'DM Mono',monospace;
        }

        .top-title {
            font-size:13px;
            color:#d4dbea;
        }

        .status-pill {
            border:1px solid #28574f;
            background:#112923;
            color:#64daca;
            border-radius:99px;
            padding:.35rem .65rem;
            font-size:11px;
        }

        h1 {
            font-size:35px !important;
            line-height:1.1 !important;
            letter-spacing:-.055em !important;
            margin:.6rem 0 .55rem !important;
        }

        .lede {
            color:#8995a9;
            font-size:14px;
            margin-bottom:1.8rem;
        }

        textarea {
            background:#0d1523 !important;
            border:1px solid #2b3850 !important;
            color:#f4f6fb !important;
            border-radius:9px !important;
            font-size:14px !important;
        }

        .section-head {
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin:2.4rem 0 .9rem;
        }

        .section-head h3 {
            font-size:14px;
            margin:0;
            letter-spacing:-.02em;
        }

        .section-meta {
            color:#69778d;
            font-size:11px;
        }

        .execution {
            border:1px solid var(--line);
            border-radius:13px;
            background:#111a29;
            overflow:hidden;
        }

        .step {
            display:flex;
            align-items:center;
            gap:.8rem;
            padding:.83rem 1rem;
            border-bottom:1px solid #202a3a;
            font-size:12px;
        }

        .step:last-child {
            border:0;
        }

        .check {
            width:21px;
            height:21px;
            display:grid;
            place-items:center;
            border-radius:50%;
            background:#153c3a;
            color:#54ddc9;
            font-size:12px;
        }

        .check.pending {
            background:#252d3c;
            color:#7b8799;
        }

        .step-title {
            font-weight:600;
            color:#d8deea;
        }

        .step-note {
            margin-left:auto;
            color:#66758b;
            font-size:10px;
            font-family:'DM Mono',monospace;
        }

        .result {
            background:#111a29;
            border:1px solid var(--line);
            border-radius:13px;
            padding:1.1rem 1.2rem;
            margin-top:1rem;
            white-space:pre-wrap;
            color:#cbd4e3;
            font-size:13px;
            line-height:1.65;
        }

        .metric {
            border:1px solid var(--line);
            background:#111a29;
            border-radius:11px;
            padding:1rem;
        }

        .metric-k {
            color:#728198;
            font-size:10px;
            text-transform:uppercase;
            letter-spacing:.1em;
        }

        .metric-v {
            font-size:22px;
            font-weight:700;
            margin-top:.3rem;
        }

        [data-testid="stButton"] button {
            border-radius:8px !important;
            border:1px solid #35415a !important;
            background:#1d2740 !important;
            color:#e6e9f4 !important;
            font-weight:700 !important;
            font-size:12px !important;
        }

        [data-testid="stButton"] button:hover {
            border-color:#8b7cff !important;
            color:#fff !important;
        }

        .run-button button {
            background:linear-gradient(135deg,#8879ff,#6454df) !important;
            border:0 !important;
            box-shadow:0 8px 20px #7162ed40;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap:1.2rem;
        }

        .stTabs [data-baseweb="tab"] {
            color:#8793a8;
        }

        .stTabs [aria-selected="true"] {
            color:#fff !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initial_state() -> None:
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("last_result", None)
    st.session_state.setdefault("active_project", "Meta-Agent Factory")
    st.session_state.setdefault("active_view", "workspace")
    st.session_state.setdefault("uploaded_pdf_path", None)


def execute_query(
    query: str,
    pdf_path: str | None = None,
) -> dict[str, Any]:
    """
    Execute the Multi-Agent workflow.

    The uploaded PDF path is passed through the shared
    LangGraph state so the RAG agent can use the document
    uploaded for the current task.
    """

    from graph.workflow import create_workflow

    state = {
        "user_query": query,
        "pdf_path": pdf_path,
        "selected_agent": "",
        "rag_result": "",
        "coding_result": {},
        "web_search_result": "",
        "final_response": "",
        "success": False,
        "error": None,
        "errors": [],
        "metadata": {},
    }

    return create_workflow().invoke(state)


def render_sidebar() -> None:
    with st.sidebar:

        st.markdown(
            '<div class="brand">'
            '<div class="brand-mark">✦</div>'
            '<div>'
            '<div class="brand-name">META FACTORY</div>'
            '<div class="brand-sub">Agent workspace</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "+  New task",
            use_container_width=True,
            key="new_task_button",
        ):
            st.session_state.last_result = None
            st.session_state.uploaded_pdf_path = None
            st.session_state.active_view = "workspace"
            st.rerun()

        st.markdown(
            '<div class="side-label">Projects</div>',
            unsafe_allow_html=True,
        )

        for name, color in [
            ("RAG Agent", ""),
            ("Web Agent", "blue"),
            ("Coding Agent", "orange"),
        ]:
            st.markdown(
                f'<div class="side-item">'
                f'<span class="project-dot {color}"></span>'
                f'{name}'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div class="side-label">Workspace</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="side-item active">'
            f'◈ &nbsp; '
            f'{html.escape(st.session_state.active_project)}'
            f'</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "◷  History",
            use_container_width=True,
            key="history_button",
        ):
            st.session_state.active_view = "history"
            st.rerun()

        if st.button(
            "⚙  Settings",
            use_container_width=True,
            key="settings_button",
        ):
            st.session_state.active_view = "settings"
            st.rerun()

        st.markdown(
            '<div class="user-card">'
            '<div class="avatar">AF</div>'
            '<div>'
            '<div class="user-name">AI Factory</div>'
            '<div class="user-role">Professional plan</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )


def render_history() -> None:
    st.markdown(
        '<div class="section-head">'
        '<h3>Recent history</h3>'
        '<div class="section-meta">Saved in this session</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.history:
        st.info("No completed tasks yet.")
        return

    for item in st.session_state.history[:8]:

        result = item.get("result", {})

        with st.expander(
            f"{item['at']}  ·  {item['query']}"
        ):

            if result.get("final_response"):

                st.markdown(
                    f'<div class="result">'
                    f'{html.escape(str(result["final_response"]))}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            elif result.get("error"):

                st.error(result["error"])

            else:

                st.caption(
                    "No generated output was saved for this task."
                )


def render_settings() -> None:
    st.markdown(
        '<div class="section-head">'
        '<h3>Settings</h3>'
        '<div class="section-meta">Workspace configuration</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "API keys are loaded from the local .env file "
        "and are never displayed here."
    )

    st.write(
        f"Active project: "
        f"{st.session_state.active_project}"
    )

    st.write(
        f"Saved history items: "
        f"{len(st.session_state.history)}"
    )


def render_execution(
    result: dict[str, Any] | None,
    running: bool = False,
) -> None:

    agent = (result or {}).get(
        "selected_agent",
        "",
    )

    has_result = bool(
        result
        and (
            result.get("final_response")
            or result.get("error")
        )
    )

    steps = [
        (
            "Orchestrator",
            "Route request to the best agent",
            bool(agent or running),
        ),
        (
            "Specialist agent",
            (
                agent.replace("_", " ").title()
                if agent
                else "Waiting for route"
            ),
            bool(agent or has_result),
        ),
        (
            "Generated output",
            "Artifacts and response assembled",
            bool(
                has_result
                and result.get("success")
            ),
        ),
        (
            "Validation",
            "Workflow completed",
            bool(
                has_result
                and result.get("success")
            ),
        ),
    ]

    body = "".join(
        f'<div class="step">'
        f'<div class="check{" pending" if not done else ""}">'
        f'{"✓" if done else "·"}'
        f'</div>'
        f'<div class="step-title">{title}</div>'
        f'<div class="step-note">{note}</div>'
        f'</div>'
        for title, note, done in steps
    )

    st.markdown(
        f'<div class="execution">{body}</div>',
        unsafe_allow_html=True,
    )


def main() -> None:

    inject_styles()
    initial_state()
    render_sidebar()

    if st.session_state.active_view == "history":
        render_history()
        return

    if st.session_state.active_view == "settings":
        render_settings()
        return

    st.markdown(
        '<div class="main-wrap">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="topbar">'
        '<div class="top-title">'
        'Meta-Agent Factory '
        '<span style="color:#526078">/</span> Workspace'
        '</div>'
        '<div class="status-pill">'
        '● All systems operational'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="eyebrow">Intelligent workspace</div>'
        '<h1>What are we building today?</h1>'
        '<div class="lede">'
        'Coordinate your agents, ship faster, and keep every result in one place.'
        '</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Task form
    # --------------------------------------------------------

    with st.form(
        "task_form",
        clear_on_submit=False,
    ):

        query = st.text_area(
            "Task prompt",
            placeholder=(
                "Ask anything... "
                "e.g. Build me a FastAPI authentication API"
            ),
            height=100,
            label_visibility="collapsed",
        )

        left, right = st.columns([4, 1])

        with left:

            uploaded = st.file_uploader(
                "Attach context",
                type=["pdf", "txt", "md"],
                label_visibility="collapsed",
            )

        with right:

            st.markdown(
                '<div class="run-button">',
                unsafe_allow_html=True,
            )

            submitted = st.form_submit_button(
                "Run task  →",
                use_container_width=True,
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # Handle uploaded document
    # --------------------------------------------------------

    if uploaded is not None:

        DOCUMENTS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        uploaded_pdf_path = (
            DOCUMENTS_DIR / uploaded.name
        )

        uploaded_pdf_path.write_bytes(
            uploaded.getbuffer()
        )

        st.session_state["uploaded_pdf_path"] = str(
            uploaded_pdf_path
        )

        st.caption(
            f"Attached: {uploaded.name}"
        )

    # --------------------------------------------------------
    # Execute task
    # --------------------------------------------------------

    if submitted:

        if not query.strip():

            st.error(
                "Enter a task before running the factory."
            )

        else:

            with st.spinner(
                "Agents are collaborating on your request..."
            ):

                started = time.perf_counter()

                try:

                    pdf_path = st.session_state.get(
                        "uploaded_pdf_path"
                    )

                    result = execute_query(
                        query.strip(),
                        pdf_path,
                    )

                    result["_duration"] = round(
                        time.perf_counter() - started,
                        2,
                    )

                    st.session_state.last_result = result

                    st.session_state.history.insert(
                        0,
                        {
                            "query": query.strip(),
                            "result": result,
                            "at": datetime.now().isoformat(
                                timespec="minutes"
                            ),
                        },
                    )

                except Exception as error:

                    st.session_state.last_result = {
                        "error": str(error),
                        "success": False,
                    }

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    result = st.session_state.last_result

    st.markdown(
        '<div class="section-head">'
        '<h3>Agent execution</h3>'
        '<div class="section-meta">Live workflow telemetry</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    render_execution(result)

    if result:

        if result.get("error"):

            st.error(
                result["error"]
            )

        if result.get("final_response"):

            st.markdown(
                '<div class="section-head">'
                '<h3>Latest response</h3>'
                '<div class="section-meta">Completed just now</div>'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="result">'
                f'{html.escape(str(result["final_response"]))}'
                f'</div>',
                unsafe_allow_html=True,
            )

        cols = st.columns(3)

        with cols[0]:

            st.markdown(
                '<div class="metric">'
                '<div class="metric-k">Status</div>'
                f'<div class="metric-v">'
                f'{"Success" if result.get("success") else "Needs review"}'
                '</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        with cols[1]:

            st.markdown(
                '<div class="metric">'
                '<div class="metric-k">Agent</div>'
                f'<div class="metric-v" style="font-size:16px">'
                f'{html.escape(str(result.get("selected_agent") or "—"))}'
                '</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        with cols[2]:

            st.markdown(
                '<div class="metric">'
                '<div class="metric-k">Duration</div>'
                f'<div class="metric-v">'
                f'{result.get("_duration", "—")}'
                '<span style="font-size:12px;color:#77859a">'
                ' sec'
                '</span>'
                '</div>'
                '</div>',
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # Run history
    # --------------------------------------------------------

    with st.expander(
        "Run history",
        expanded=bool(st.session_state.history),
    ):

        if not st.session_state.history:

            st.caption(
                "Your completed tasks will appear here."
            )

        for item in st.session_state.history[:8]:

            st.markdown(
                f"**{item['at']}**  ·  {item['query']}"
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

