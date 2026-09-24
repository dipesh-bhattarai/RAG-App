import uuid
import html
import requests
import streamlit as st


# ============================================================
# CONFIG
# ============================================================

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="RAG Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "documents" not in st.session_state:
    st.session_state.documents = []

if "show_sources" not in st.session_state:
    st.session_state.show_sources = True

if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ========================================================
       GLOBAL
       ======================================================== */

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background: #212121 !important;
        color: #ececec !important;
    }

    .stApp { background: #212121 !important; }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    #MainMenu, footer { visibility: hidden; }

    [data-testid="stAppViewBlockContainer"] {
        padding-top: 1.5rem !important;
        max-width: 900px;
    }

    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #171717 !important;
        border-right: 1px solid #2a2a2a !important;
    }

    section[data-testid="stSidebar"] > div {
        background: #171717 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #ececec !important;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 6px 4px 20px 4px;
    }

    .brand-icon {
        width: 32px;
        height: 32px;
        border-radius: 9px;
        background: linear-gradient(135deg, #10a37f, #1a7f64);
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 17px;
        font-weight: 700;
        box-shadow: 0 2px 8px rgba(16, 163, 127, 0.35);
    }

    .brand-name {
        font-size: 16px;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: -0.2px;
    }

    /* ========================================================
       SIDEBAR BUTTONS
       ======================================================== */

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: transparent !important;
        color: #ececec !important;
        border: 1px solid #333333 !important;
        border-radius: 10px !important;
        text-align: left !important;
        height: 42px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        transition: all 0.15s ease !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #262626 !important;
        border-color: #10a37f !important;
    }

    /* ========================================================
       SIDEBAR HEADINGS
       ======================================================== */

    .sidebar-heading {
        color: #8a8a8a;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 24px 0 10px 2px;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #2a2a2a !important;
        margin: 10px 0 !important;
    }

    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: #1c1c1c !important;
        border: 1.5px dashed #3a3a3a !important;
        border-radius: 10px !important;
        padding: 6px !important;
        transition: border-color 0.15s ease;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
        border-color: #10a37f !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploader"] section {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] span,
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] small {
        color: #9b9b9b !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
        background: #2a2a2a !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
        border-radius: 7px !important;
    }

    /* ========================================================
       DOCUMENT CARDS
       ======================================================== */

    .document-card {
        display: flex;
        align-items: center;
        gap: 9px;
        background: #1c1c1c;
        border: 1px solid #2e2e2e;
        border-radius: 9px;
        padding: 10px 11px;
        margin: 6px 0;
        transition: border-color 0.15s ease;
    }

    .document-card:hover {
        border-color: #454545;
    }

    .document-icon {
        flex-shrink: 0;
        width: 26px;
        height: 26px;
        border-radius: 6px;
        background: rgba(16, 163, 127, 0.12);
        color: #10a37f;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
    }

    .document-name {
        font-size: 13px;
        color: #e5e5e5;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        flex: 1;
    }

    .empty-state {
        color: #6b6b6b;
        font-size: 12.5px;
        text-align: center;
        padding: 18px 8px;
        border: 1px dashed #2e2e2e;
        border-radius: 9px;
        margin-top: 8px;
    }

    /* ========================================================
       WELCOME
       ======================================================== */

    .welcome-container {
        min-height: 62vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    .welcome-icon {
        width: 60px;
        height: 60px;
        border-radius: 16px;
        background: linear-gradient(135deg, #10a37f, #1a7f64);
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 22px;
        box-shadow: 0 4px 18px rgba(16, 163, 127, 0.3);
    }

    .welcome-title {
        font-size: 28px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 8px;
        letter-spacing: -0.4px;
    }

    .welcome-subtitle {
        font-size: 14.5px;
        color: #8e8e8e;
        max-width: 420px;
    }

    .suggestion-grid {
        display: flex;
        gap: 10px;
        margin-top: 26px;
        flex-wrap: wrap;
        justify-content: center;
    }

    .suggestion-chip {
        background: #1c1c1c;
        border: 1px solid #333333;
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 12.5px;
        color: #b0b0b0;
    }

    /* ========================================================
       CHAT MESSAGES  (st.chat_message)
       ======================================================== */

    [data-testid="stChatMessage"] {
        background: transparent !important;
        padding: 10px 0 !important;
        gap: 14px !important;
        border: none !important;
    }

    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
        width: 30px !important;
        height: 30px !important;
        border-radius: 9px !important;
    }

    [data-testid="stChatMessageAvatarAssistant"] {
        background: linear-gradient(135deg, #10a37f, #1a7f64) !important;
    }

    [data-testid="stChatMessageAvatarUser"] {
        background: #5a5a5a !important;
    }

    [data-testid="stChatMessageContent"] {
        color: #ececec !important;
    }

    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] li {
        font-size: 15px !important;
        line-height: 1.65 !important;
        color: #ececec !important;
    }

    /* user bubble look */
    .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
        background: #2f2f2f;
        border-radius: 18px;
        padding: 11px 16px;
        display: inline-block;
        max-width: 80%;
    }

    .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) {
        display: flex;
        flex-direction: row-reverse;
        justify-content: flex-start;
    }

    /* code blocks inside messages */
    [data-testid="stChatMessageContent"] pre {
        background: #171717 !important;
        border: 1px solid #2e2e2e !important;
        border-radius: 10px !important;
    }

    [data-testid="stChatMessageContent"] code {
        color: #7ee2c3 !important;
    }

    /* ========================================================
       SOURCES
       ======================================================== */

    .sources-title {
        color: #8e8e8e;
        font-size: 12px;
        margin-top: 6px;
        margin-bottom: 7px;
    }

    .source-card {
        background: #1c1c1c;
        border: 1px solid #2e2e2e;
        border-left: 3px solid #10a37f;
        border-radius: 8px;
        padding: 10px 12px;
        margin: 6px 0;
        color: #b7b7b7;
        font-size: 12.5px;
        line-height: 1.55;
    }

    .source-label {
        color: #10a37f;
        font-weight: 600;
        font-size: 11.5px;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    /* ========================================================
       TYPING INDICATOR
       ======================================================== */

    .typing-dots {
        display: flex;
        gap: 4px;
        padding: 8px 0 4px 0;
    }

    .typing-dots span {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #8e8e8e;
        animation: typing-bounce 1.1s infinite ease-in-out;
    }

    .typing-dots span:nth-child(2) { animation-delay: 0.15s; }
    .typing-dots span:nth-child(3) { animation-delay: 0.3s; }

    @keyframes typing-bounce {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
        30% { transform: translateY(-5px); opacity: 1; }
    }

    /* ========================================================
       CHAT INPUT
       ======================================================== */

    [data-testid="stChatInput"] {
        background: transparent !important;
    }

    [data-testid="stChatInput"] > div {
        background: #2a2a2a !important;
        border: 1px solid #444444 !important;
        border-radius: 26px !important;
        box-shadow: 0 4px 18px rgba(0,0,0,0.25) !important;
    }

    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: #ffffff !important;
        font-size: 15px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #8e8e8e !important;
    }

    [data-testid="stChatInput"] button {
        background: #10a37f !important;
        color: #ffffff !important;
        border-radius: 50% !important;
    }

    .input-disclaimer {
        text-align: center;
        color: #6b6b6b;
        font-size: 11.5px;
        margin-top: 10px;
    }

    /* ========================================================
       ALERTS / EXPANDER / TOGGLE
       ======================================================== */

    [data-testid="stAlert"] {
        background: #262626 !important;
        border: 1px solid #383838 !important;
        color: #ececec !important;
        border-radius: 10px !important;
    }

    [data-testid="stExpander"] {
        background: #1c1c1c !important;
        border: 1px solid #2e2e2e !important;
        border-radius: 10px !important;
    }

    [data-testid="stExpander"] summary {
        color: #b7b7b7 !important;
        font-size: 13px !important;
    }

    [data-testid="stToggle"] label {
        color: #d0d0d0 !important;
        font-size: 13.5px !important;
    }

    /* ========================================================
       SPINNER
       ======================================================== */

    [data-testid="stSpinner"] p {
        color: #8e8e8e !important;
        font-size: 13.5px !important;
    }

    /* ========================================================
       SCROLLBAR
       ======================================================== */

    ::-webkit-scrollbar { width: 7px; height: 7px; }
    ::-webkit-scrollbar-track { background: #212121; }
    ::-webkit-scrollbar-thumb { background: #444444; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #555555; }

    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {
        .welcome-title { font-size: 23px; }
        .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
            max-width: 90%;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def create_new_chat():
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())


def load_documents():
    try:
        response = requests.get(f"{BACKEND_URL}/document/", timeout=20)
        if response.ok:
            data = response.json()
            st.session_state.documents = data if isinstance(data, list) else []
        else:
            st.session_state.documents = []
    except requests.exceptions.RequestException:
        st.session_state.documents = []


def upload_document(uploaded_file):
    try:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type or "application/pdf",
            )
        }
        response = requests.post(f"{BACKEND_URL}/upload/", files=files, timeout=300)

        if response.ok:
            return True, response.json()

        try:
            error = response.json().get("detail", response.text)
        except Exception:
            error = response.text
        return False, error

    except requests.exceptions.RequestException:
        return False, "Backend is not reachable."


def send_question(question):
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat/",
            json={"question": question, "session_id": st.session_state.session_id},
            timeout=300,
        )

        if response.ok:
            data = response.json()
            return (
                data.get("answer", "I couldn't generate an answer."),
                data.get("sources", []),
            )

        try:
            error = response.json().get("detail", response.text)
        except Exception:
            error = response.text
        return f"Backend error: {error}", []

    except requests.exceptions.RequestException:
        return (
            "⚠️ I couldn't connect to the RAG backend. "
            "Make sure FastAPI is running on port 8000.",
            [],
        )


def delete_document(document_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/document/{document_id}", timeout=30)
        return response.ok
    except requests.exceptions.RequestException:
        return False


def file_icon(filename):
    ext = str(filename).lower().rsplit(".", 1)[-1] if "." in str(filename) else ""
    return {"pdf": "📕", "docx": "📘", "txt": "📄", "csv": "📊"}.get(ext, "📄")


def render_sources(sources):
    st.markdown(
        f'<div class="sources-title">📚 SOURCES · {len(sources)}</div>',
        unsafe_allow_html=True,
    )
    for index, source in enumerate(sources, start=1):
        if isinstance(source, dict):
            source_text = source.get("text", "")
            page = source.get("page") or source.get("page_number")
            filename = source.get("filename") or source.get("source")
        else:
            source_text, page, filename = str(source), None, None

        safe_source = html.escape(source_text)
        label_bits = [f"Source {index}"]
        if filename:
            label_bits.append(html.escape(str(filename)))
        if page:
            label_bits.append(f"p.{page}")
        label = " · ".join(label_bits)

        st.markdown(
            f"""
            <div class="source-card">
                <div class="source-label">{label}</div>
                <div style="margin-top:5px;">{safe_source}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">✦</div>
            <div class="brand-name">RAG Assistant</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("＋  New chat", use_container_width=True):
        create_new_chat()
        st.rerun()

    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    st.markdown('<div class="sidebar-heading">Documents</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        st.markdown(
            f"""
            <div class="document-card">
                <div class="document-icon">📕</div>
                <div class="document-name">{html.escape(uploaded_file.name)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Process document", use_container_width=True):
            with st.spinner("Processing document..."):
                success, result = upload_document(uploaded_file)

            if success:
                st.success("Document processed successfully.")
                load_documents()
            else:
                st.error(str(result))

    load_documents()

    if st.session_state.documents:
        for document in st.session_state.documents:
            document_id = document.get("document_id") or document.get("id")
            filename = (
                document.get("filename")
                or document.get("name")
                or document.get("file_name")
                or "Document"
            )

            col1, col2 = st.columns([5, 1.3])
            with col1:
                st.markdown(
                    f"""
                    <div class="document-card">
                        <div class="document-icon">{file_icon(filename)}</div>
                        <div class="document-name" title="{html.escape(str(filename))}">
                            {html.escape(str(filename))}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col2:
                if document_id and st.button("✕", key=f"delete_{document_id}"):
                    if delete_document(document_id):
                        st.success("Deleted.")
                        load_documents()
                        st.rerun()
                    else:
                        st.error("Could not delete document.")
    else:
        st.markdown(
            '<div class="empty-state">No documents yet.<br>Upload a PDF to get started.</div>',
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # SETTINGS
    # --------------------------------------------------------

    st.markdown('<div class="sidebar-heading">Settings</div>', unsafe_allow_html=True)

    st.session_state.show_sources = st.toggle(
        "Show sources",
        value=st.session_state.show_sources,
    )

    st.markdown(
        """
        <div style="position: fixed; bottom: 15px; color: #666; font-size: 11px;">
            RAG Assistant · Local
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-container">
            <div class="welcome-icon">✦</div>
            <div class="welcome-title">How can I help you?</div>
            <div class="welcome-subtitle">
                Ask questions about your uploaded documents and I'll answer
                using only what's inside them.
            </div>
            <div class="suggestion-grid">
                <div class="suggestion-chip">📄 Summarize a document</div>
                <div class="suggestion-chip">🔍 Find a specific fact</div>
                <div class="suggestion-chip">🧩 Compare two sections</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="✨"):
            st.markdown(message["content"])

            sources = message.get("sources", [])
            if st.session_state.show_sources and sources:
                with st.expander(f"📚 Sources ({len(sources)})"):
                    render_sources(sources)


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input("Message RAG Assistant...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="✨"):
        placeholder = st.empty()
        placeholder.markdown(
            """
            <div class="typing-dots"><span></span><span></span><span></span></div>
            """,
            unsafe_allow_html=True,
        )

        answer, sources = send_question(prompt)
        placeholder.markdown(answer)

        if st.session_state.show_sources and sources:
            with st.expander(f"📚 Sources ({len(sources)})"):
                render_sources(sources)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )

    st.rerun()