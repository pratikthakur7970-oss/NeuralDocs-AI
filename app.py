import os
import streamlit as st
import html

# =========================================================
# IMPORT EXISTING RAG MODULES
# =========================================================
from llms.groq_llama import get_groq_llm
from loaders.pdf_loader import load_and_split_pdf
from retrievers.retriever import create_vector_store
from UI.splash import show_splash
from UI.Login import show_login
from UI.Signup import show_signup
from UI.Admin import show_admin
from Auth.auth_manager import init_db


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="NeuralDocs | AI Research Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize authentication database once per app run.
init_db()

# Show animated splash screen once per session.
show_splash()

# Authentication routing.
if not st.session_state.get("authenticated", False):
    current_page = st.session_state.get("auth_page", "login")

    if current_page == "signup":
        show_signup()
    else:
        show_login()

    st.stop()

# Get authenticated user.
current_user = st.session_state.get("user", {})


# =========================================================
# CUSTOM PREMIUM CSS
# =========================================================
st.markdown("""
<style>

/* ---------- GLOBAL ---------- */
.stApp {
    background: #080d19;
    color: #e5e7eb;
}

header[data-testid="stHeader"] {
    background: rgba(8, 13, 25, 0.95);
}

#MainMenu, footer {
    visibility: hidden;
}


/* REMOVE TOP GAP */
.block-container {
    max-width: 1250px;
    padding-top: 0rem !important;
    padding-bottom: 1rem;
    margin-top: 0rem !important;
}

/* Reduce Streamlit header spacing */
header[data-testid="stHeader"] {
    height: 0rem !important;
    background: transparent !important;
}


/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111a2e 0%, #0b1120 100%);
    border-right: 1px solid #26334d;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

.sidebar-brand {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #ffffff;
    margin-bottom: 5px;
}

.sidebar-caption {
    font-size: 12px;
    color: #8998b5;
    margin-bottom: 30px;
}

.sidebar-label {
    color: #8998b5;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-top: 22px;
    margin-bottom: 12px;
}

.info-card {
    background: #18243a;
    border: 1px solid #2b3b58;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 10px;
}

.info-title {
    color: #8998b5;
    font-size: 11px;
    margin-bottom: 5px;
}

.info-value {
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
}

/* ---------- MAIN HEADER ---------- */
.top-badge {
    display: inline-block;
    background: rgba(99, 102, 241, 0.12);
    color: #a5b4fc;
    border: 1px solid rgba(129, 140, 248, 0.3);
    padding: 7px 14px;
    border-radius: 30px;
    font-size: 12px;
    margin-bottom: 18px;
}

.main-title {
    font-size: 43px;
    font-weight: 850;
    letter-spacing: -2px;
    line-height: 1.2;
    color: white;
    margin-bottom: 10px;
}

.gradient-text {
    background: linear-gradient(90deg, #818cf8, #c084fc, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.main-subtitle {
    color: #94a3b8;
    font-size: 15px;
    line-height: 1.8;
    margin-bottom: 25px;
}

/* ---------- STATUS CARDS ---------- */
.status-card {
    background: linear-gradient(145deg, #141f35, #101829);
    border: 1px solid #263650;
    border-radius: 14px;
    padding: 17px;
    min-height: 85px;
}

.status-label {
    font-size: 11px;
    color: #8998b5;
    margin-bottom: 8px;
}

.status-value {
    font-size: 15px;
    font-weight: 700;
    color: #e2e8f0;
}

/* ---------- SECTION HEADING ---------- */
.section-heading {
    color: #f1f5f9;
    font-size: 17px;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 15px;
}

/* ---------- CHAT MESSAGES ---------- */
.stChatMessage {
    background: #121d31;
    border: 1px solid #293953;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 15px;
}

[data-testid="stChatMessage"] p {
    color: #e2e8f0;
    line-height: 1.8;
}


/* ---------- PREMIUM CHAT INPUT ---------- */

div[data-testid="stChatInput"] {
    background: #111827 !important;
    border: 1px solid #475569 !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
    transition: all 0.3s ease;
}

div[data-testid="stChatInput"]:focus-within {
    border: 1px solid #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
}

div[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #f1f5f9 !important;
    caret-color: #a5b4fc !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #94a3b8 !important;
    opacity: 1 !important;
}

div[data-testid="stChatInput"] button {
    background: #6366f1 !important;
    color: white !important;
    border-radius: 10px !important;
}

div[data-testid="stChatInput"] button:hover {
    background: #818cf8 !important;
}

/* Chat message containers */
div[data-testid="stChatMessage"] {
    background: #111c30 !important;
    border: 1px solid #263650 !important;
    border-radius: 16px !important;
    padding: 18px !important;
    margin-bottom: 14px !important;
}

div[data-testid="stChatMessage"] p {
    color: #e2e8f0 !important;
    line-height: 1.8;
}

/* ---------- BUTTONS ---------- */
.stButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 10px 15px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    border: none;
    transform: translateY(-2px);
}

/* ---------- EXPANDER ---------- */
.streamlit-expanderHeader {
    background: #162239;
    border-radius: 10px;
    color: #cbd5e1;
}

[data-testid="stExpander"] {
    border: 1px solid #293953;
    border-radius: 12px;
}

/* ---------- DIVIDER ---------- */
hr {
    border-color: #263650;
}

/* ---------- FOOTER ---------- */
.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 25px 0 10px 0;
}

/* =====================================
   FIX STREAMLIT BOTTOM WHITE BACKGROUND
===================================== */

/* Main bottom fixed container */
[data-testid="stBottom"] {
    background: #080d19 !important;
    background-color: #080d19 !important;
}

/* Floating chat input wrapper */
.stChatFloatingInputContainer {
    background: #080d19 !important;
    background-color: #080d19 !important;
    padding-top: 12px !important;
    padding-bottom: 12px !important;
}

/* Bottom block container */
[data-testid="stBottomBlockContainer"] {
    background: #080d19 !important;
}

/* Chat input outer box */
[data-testid="stChatInput"] {
    background: #111827 !important;
    border: 1px solid #475569 !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
}

/* Inner textarea */
[data-testid="stChatInput"] [data-baseweb="textarea"] {
    background: #111827 !important;
}

/* Actual text area */
[data-testid="stChatInput"] textarea {
    background: #111827 !important;
    color: #f1f5f9 !important;
    -webkit-text-fill-color: #f1f5f9 !important;
}

/* Placeholder */
[data-testid="stChatInput"] textarea::placeholder {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
}

/* Remove white background from inner wrappers */
[data-testid="stChatInput"] div {
    background-color: transparent;
}

[data-testid="stChatInput"] [data-baseweb="textarea"] {
    background-color: #111827 !important;
}

/* =====================================
   FIX DARK TEXT IN AI RESPONSE
===================================== */

/* All chat response text */
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    color: #e2e8f0 !important;
}

/* Headings */
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4 {
    color: #f8fafc !important;
    font-weight: 700 !important;
}

/* Paragraphs and lists */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    color: #e2e8f0 !important;
    line-height: 1.8 !important;
}

/* Tables */
[data-testid="stChatMessage"] table {
    background: #18243a !important;
    color: #f1f5f9 !important;
    border-collapse: collapse !important;
}

[data-testid="stChatMessage"] th {
    background: #263650 !important;
    color: #ffffff !important;
}

[data-testid="stChatMessage"] td {
    background: #18243a !important;
    color: #e2e8f0 !important;
    border: 1px solid #475569 !important;
}

/* Inline code */
[data-testid="stChatMessage"] code {
    background: #263650 !important;
    color: #c4b5fd !important;
}

/* Links */
[data-testid="stChatMessage"] a {
    color: #93c5fd !important;
}

/* Bold text */
[data-testid="stChatMessage"] strong {
    color: #ffffff !important;
}

/* ABOUT AND ACCOUNT DARK PANELS */
.sidebar-footer-card {
    background: linear-gradient(
        145deg,
        #17243a,
        #101a2d
    ) !important;
    border: 1px solid #2b3b58 !important;
    border-radius: 13px;
    padding: 15px;
    margin-top: 12px;
    margin-bottom: 12px;
}

.sidebar-footer-title {
    color: #a5b4fc;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

.sidebar-footer-text {
    color: #d1d9e6;
    font-size: 12px;
    line-height: 1.8;
}

.sidebar-footer-version {
    color: #8493ad;
    font-size: 11px;
    margin-top: 10px;
}

.sidebar-account-email {
    color: #e2e8f0;
    font-size: 12px;
    overflow-wrap: anywhere;
    margin-top: 7px;
}
/* MATHEMATICAL FORMULA DISPLAY */

[data-testid="stChatMessage"] .katex {
    color: #e2e8f0 !important;
    font-size: 1.05em;
}

[data-testid="stChatMessage"] .katex-display {
    overflow-x: auto;
    overflow-y: hidden;
    padding: 12px 4px;
    margin: 15px 0;
    background: #17243a;
    border-radius: 10px;
}

[data-testid="stChatMessage"] pre {
    background: #17243a !important;
    border: 1px solid #334155;
    border-radius: 12px;
}

[data-testid="stChatMessage"] table {
    width: 100%;
    border-collapse: collapse;
    color: #e2e8f0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# RAG PIPELINE INITIALIZATION
# =========================================================
@st.cache_resource(show_spinner=False)
def initialize_rag_pipeline():

    pdf_path = os.path.join(
        "data",
        "raw",
        "attention_is_all_you_need.pdf"
    )

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    chunks = load_and_split_pdf(pdf_path)
    retriever = create_vector_store(chunks)
    llm = get_groq_llm()

    return retriever, llm


# =========================================================
# SESSION STATE
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 Welcome to NeuralDocs. "
                "I am your AI research assistant. "
                "Ask me anything about the "
                "Attention Is All You Need research paper."
            ),
            "sources": []
        }
    ]


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    # BRAND
    st.markdown(
        '<div class="sidebar-brand">✦ NeuralDocs AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-caption">'
        'Intelligent Research Assistant'
        '</div>',
        unsafe_allow_html=True
    )

    # SYSTEM OVERVIEW
    st.markdown(
        '<div class="sidebar-label">SYSTEM OVERVIEW</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-card">
        <div class="info-title">LANGUAGE MODEL</div>
        <div class="info-value">⚡ Llama 3 · Groq API</div>
    </div>

    <div class="info-card">
        <div class="info-title">VECTOR DATABASE</div>
        <div class="info-value">🗄️ ChromaDB / Configured Store</div>
    </div>

    <div class="info-card">
        <div class="info-title">DOCUMENT</div>
        <div class="info-value">📄 Attention Is All You Need</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # CHAT CONTROLS
    st.markdown(
        '<div class="sidebar-label">CHAT CONTROLS</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "🧹 Clear Chat History",
        use_container_width=True,
        key="clear_chat_history"
    ):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! 👋 Your chat has been cleared. "
                    "What would you like to know?"
                ),
                "sources": []
            }
        ]
        st.rerun()

    # ADMIN DASHBOARD - ADMIN ONLY
    user_role = str(current_user.get("role", "")).strip().lower()

    if user_role == "admin":
        st.markdown("---")
        st.markdown(
            '<div class="sidebar-label">ADMINISTRATION</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "🛡️ Admin Dashboard",
            use_container_width=True,
            key="admin_dashboard_button"
        ):
            st.session_state["app_page"] = "admin"
            st.rerun()

    # ABOUT PANEL - kept once
    st.markdown("---")
    st.markdown("""
    <div class="sidebar-footer-card">
        <div class="sidebar-footer-title">
            ABOUT
        </div>
        <div class="sidebar-footer-text">
            NeuralDocs AI is a Retrieval Augmented Generation
            application built with LangChain, Groq and Streamlit.
        </div>
        <div class="sidebar-footer-version">
            Version 1.0.0 · Made with ❤️
        </div>
    </div>
    """, unsafe_allow_html=True)

    # SIGNED IN AS PANEL - kept once
    user_email = html.escape(str(current_user.get("email", "")))
    st.markdown(f"""
    <div class="sidebar-footer-card">
        <div class="sidebar-footer-title">
            SIGNED IN AS
        </div>
        <div class="sidebar-account-email">
            {user_email}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # LOGOUT BUTTON - kept once
    if st.button(
        "🚪 Logout",
        use_container_width=True,
        key="sidebar_logout"
    ):
        st.session_state.pop("authenticated", None)
        st.session_state.pop("user", None)
        st.session_state.pop("messages", None)
        st.session_state.pop("pending_prompt", None)
        st.session_state.pop("app_page", None)
        st.session_state["auth_page"] = "login"
        st.rerun()


# =========================================================
# ADMIN PAGE ROUTING
# =========================================================
if st.session_state.get("app_page") == "admin":

    # Server-side role check: do not trust the sidebar visibility alone.
    if str(current_user.get("role", "")).strip().lower() != "admin":
        st.session_state.pop("app_page", None)
        st.error("Access denied. Admin permission required.")
        st.stop()

    show_admin()
    st.stop()


# =========================================================
# MAIN HEADER
# =========================================================
st.markdown(
    '<div class="top-badge">✦ AI POWERED RESEARCH ASSISTANT</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-title">
        Attention Is <span class="gradient-text">All You Need.</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-subtitle">
        Explore the revolutionary Transformer architecture.
        Ask questions, discover insights, and understand the research
        paper with your intelligent RAG assistant.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INITIALIZE BACKEND
# =========================================================
try:

    with st.spinner("Initializing your AI research assistant..."):
        retriever, llm = initialize_rag_pipeline()

    pipeline_ready = True

except Exception as e:

    pipeline_ready = False
    retriever = None
    llm = None

    st.error(f"Pipeline initialization failed: {e}")


# =========================================================
# STATUS OVERVIEW
# =========================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="status-card">
        <div class="status-label">AI ENGINE</div>
        <div class="status-value">⚡ Groq · Llama</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="status-card">
        <div class="status-label">KNOWLEDGE SOURCE</div>
        <div class="status-value">📚 Research PDF</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    status_text = "🟢 Online" if pipeline_ready else "🔴 Offline"

    st.markdown(f"""
    <div class="status-card">
        <div class="status-label">PIPELINE STATUS</div>
        <div class="status-value">{status_text}</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# SUGGESTED QUESTIONS
# =========================================================
st.markdown(
    '<div class="section-heading">💡 Explore the Research Paper</div>',
    unsafe_allow_html=True
)

suggestions = [
    "What is the Transformer architecture?",
    "Explain self-attention mechanism.",
    "What is multi-head attention?",
    "Why does Transformer use positional encoding?"
]

suggestion_cols = st.columns(2)

for i, question in enumerate(suggestions):

    with suggestion_cols[i % 2]:

        if st.button(
            question,
            key=f"suggestion_{i}",
            use_container_width=True
        ):
            st.session_state.pending_prompt = question
            st.rerun()


# =========================================================
# CHAT HISTORY DISPLAY
# =========================================================
st.markdown(
    '<div class="section-heading">💬 Research Conversation</div>',
    unsafe_allow_html=True
)

for message in st.session_state.messages:

    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):

        st.markdown(message["content"])

        sources = message.get("sources", [])

        if sources:

            with st.expander(
                f"📚 View Retrieved Sources ({len(sources)})"
            ):

                for idx, doc in enumerate(sources):

                    st.markdown(f"**Source Chunk {idx + 1}**")

                    st.text(
                        doc[:1000]
                    )

                    if idx < len(sources) - 1:
                        st.divider()


# =========================================================
# USER INPUT
# =========================================================
prompt = st.chat_input(
    "Ask anything about the Transformer research paper..."
)

if "pending_prompt" in st.session_state:

    prompt = st.session_state.pop("pending_prompt")


# =========================================================
# GENERATE RESPONSE
# =========================================================
if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "sources": []
    })

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):

        if not pipeline_ready:

            response_text = (
                "The RAG pipeline is currently unavailable. "
                "Please check the PDF path, database configuration "
                "and API credentials."
            )

            source_texts = []

            st.error(response_text)

        else:

            try:

                with st.spinner(
                    "🔍 Searching knowledge base and generating answer..."
                ):

                    # 1. Retrieve relevant documents
                    relevant_docs = retriever.invoke(prompt)

                    # 2. Build context
                    context = "\n\n".join(
                        doc.page_content
                        for doc in relevant_docs
                    )

                    # 3. Build final prompt
                    final_prompt = f"""
You are an expert research assistant specializing in
the Attention Is All You Need paper.

Answer the user's question using the provided context.

Instructions:
- Give clear and accurate explanations.
- Use headings and bullet points where useful.
- If the answer is not available in the context,
  clearly mention that.
- Do not invent information.

Context:
{context}

Question:
{prompt}

Answer:
"""

                    # 4. Generate answer
                    raw_response = llm.invoke(final_prompt)

                    if hasattr(raw_response, "content"):
                        response_text = raw_response.content
                    else:
                        response_text = str(raw_response)

                    source_texts = [
                        doc.page_content
                        for doc in relevant_docs
                    ]

                st.markdown(response_text)

                if source_texts:

                    with st.expander(
                        f"📚 View Retrieved Sources ({len(source_texts)})"
                    ):

                        for idx, source in enumerate(source_texts):

                            st.markdown(
                                f"**Source Chunk {idx + 1}**"
                            )

                            st.text(source[:1000])

                            if idx < len(source_texts) - 1:
                                st.divider()

            except Exception as e:

                response_text = (
                    f"An error occurred while generating "
                    f"the answer: {str(e)}"
                )

                source_texts = []

                st.error(response_text)

    # Save response and sources
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "sources": source_texts
    })

    st.rerun()


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.markdown(
    """
    <div class="footer">
        ✦ NeuralDocs AI · Powered by Groq, Llama & Retrieval Augmented Generation
        <br><br>
        Built for intelligent research and document understanding.
    </div>
    """,
    unsafe_allow_html=True
)
