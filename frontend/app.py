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


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {
        background: #212121 !important;
        color: #ececec !important;
    }

    .stApp {
        background: #212121 !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #171717 !important;
        border-right: 1px solid #2f2f2f !important;
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
        padding: 8px 4px 18px 4px;
    }

    .brand-icon {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: #ffffff;
        color: #171717;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 17px;
        font-weight: 700;
    }

    .brand-name {
        font-size: 17px;
        font-weight: 600;
        color: #ffffff;
    }


    /* ========================================================
       SIDEBAR BUTTON
       ======================================================== */

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;

        background: transparent !important;
        color: #ececec !important;

        border: 1px solid #3a3a3a !important;
        border-radius: 8px !important;

        text-align: left !important;

        height: 42px !important;

        font-size: 14px !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #2a2a2a !important;
        border-color: #4a4a4a !important;
    }


    /* ========================================================
       SIDEBAR HEADINGS
       ======================================================== */

    .sidebar-heading {
        color: #8e8e8e;

        font-size: 12px;
        font-weight: 600;

        text-transform: uppercase;
        letter-spacing: 0.5px;

        margin: 22px 0 10px 2px;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #2f2f2f !important;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    section[data-testid="stSidebar"]
    [data-testid="stFileUploader"] {
        background: #212121 !important;

        border: 1px solid #3a3a3a !important;

        border-radius: 9px !important;

        padding: 5px !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stFileUploader"] section {
        background: #212121 !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stFileUploader"] button {
        background: #2f2f2f !important;

        color: #ffffff !important;

        border: 1px solid #444444 !important;
    }


    /* ========================================================
       DOCUMENT CARDS
       ======================================================== */

    .document-card {
        background: #212121;

        border: 1px solid #343434;

        border-radius: 8px;

        padding: 10px;

        margin: 7px 0;
    }

    .document-name {
        font-size: 13px;
        color: #e5e5e5;

        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }


    /* ========================================================
       MAIN CONTAINER
       ======================================================== */

    .main-container {
        max-width: 850px;

        margin: 0 auto;

        padding: 0 20px 140px 20px;
    }


    /* ========================================================
       WELCOME
       ======================================================== */

    .welcome-container {
        min-height: 68vh;

        display: flex;
        flex-direction: column;

        align-items: center;
        justify-content: center;

        text-align: center;
    }

    .welcome-icon {
        width: 58px;
        height: 58px;

        border-radius: 50%;

        background: #ffffff;
        color: #171717;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 28px;
        font-weight: 700;

        margin-bottom: 22px;
    }

    .welcome-title {
        font-size: 30px;

        font-weight: 600;

        color: #ffffff;

        margin-bottom: 10px;
    }

    .welcome-subtitle {
        font-size: 15px;

        color: #9b9b9b;
    }


    /* ========================================================
       USER MESSAGE
       ======================================================== */

    .message-row {
        display: flex;

        width: 100%;

        margin: 28px 0;
    }

    .message-row.user {
        justify-content: flex-end;
    }

    .message-row.assistant {
        justify-content: flex-start;
    }

    .user-bubble {
        max-width: 72%;

        background: #2f2f2f;

        color: #ececec;

        padding: 11px 16px;

        border-radius: 18px;

        font-size: 15px;

        line-height: 1.55;

        word-wrap: break-word;
    }


    /* ========================================================
       ASSISTANT
       ======================================================== */

    .assistant-wrapper {
        display: flex;

        align-items: flex-start;

        gap: 14px;

        width: 100%;
    }

    .assistant-avatar {
        flex-shrink: 0;

        width: 30px;
        height: 30px;

        border-radius: 50%;

        background: #ffffff;
        color: #171717;

        display: flex;

        align-items: center;
        justify-content: center;

        font-size: 15px;

        font-weight: 700;

        margin-top: 2px;
    }

    .assistant-content {
        max-width: 780px;

        color: #ececec;

        font-size: 15px;

        line-height: 1.7;
    }


    /* ========================================================
       SOURCES
       ======================================================== */

    .sources-title {
        color: #8e8e8e;

        font-size: 12px;

        margin-top: 15px;

        margin-bottom: 7px;
    }

    .source-card {
        background: #2a2a2a;

        border: 1px solid #3a3a3a;

        border-radius: 8px;

        padding: 9px 11px;

        margin: 5px 0;

        color: #bdbdbd;

        font-size: 12px;

        line-height: 1.5;
    }


    /* ========================================================
       CHAT INPUT
       ======================================================== */

    [data-testid="stChatInput"] {
        background: transparent !important;
    }

    [data-testid="stChatInput"] > div {
        background: #2f2f2f !important;

        border: 1px solid #4a4a4a !important;

        border-radius: 26px !important;

        box-shadow: none !important;
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
        background: #ffffff !important;

        color: #171717 !important;

        border-radius: 50% !important;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    [data-testid="stAlert"] {
        background: #2a2a2a !important;

        border: 1px solid #3a3a3a !important;

        color: #ececec !important;
    }


    /* ========================================================
       EXPANDER
       ======================================================== */

    [data-testid="stExpander"] {
        background: #242424 !important;

        border: 1px solid #363636 !important;

        border-radius: 8px !important;
    }

    [data-testid="stExpander"] summary {
        color: #bdbdbd !important;
    }


    /* ========================================================
       TOGGLE
       ======================================================== */

    [data-testid="stToggle"] label {
        color: #bdbdbd !important;
    }


    /* ========================================================
       SCROLLBAR
       ======================================================== */

    ::-webkit-scrollbar {
        width: 7px;
    }

    ::-webkit-scrollbar-track {
        background: #212121;
    }

    ::-webkit-scrollbar-thumb {
        background: #444444;

        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #555555;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .main-container {
            padding-left: 12px;
            padding-right: 12px;
        }

        .user-bubble {
            max-width: 85%;
        }

        .welcome-title {
            font-size: 25px;
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
        response = requests.get(
            f"{BACKEND_URL}/document/",
            timeout=20,
        )

        if response.ok:
            data = response.json()

            if isinstance(data, list):
                st.session_state.documents = data
            else:
                st.session_state.documents = []

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

        response = requests.post(
            f"{BACKEND_URL}/upload/",
            files=files,
            timeout=300,
        )

        if response.ok:
            return True, response.json()

        try:
            error = response.json().get(
                "detail",
                response.text,
            )
        except Exception:
            error = response.text

        return False, error

    except requests.exceptions.RequestException:
        return False, "Backend is not reachable."


def send_question(question):

    try:

        response = requests.post(
            f"{BACKEND_URL}/chat/",
            json={
                "question": question,
                "session_id": st.session_state.session_id,
            },
            timeout=300,
        )

        if response.ok:

            data = response.json()

            return (
                data.get(
                    "answer",
                    "I couldn't generate an answer.",
                ),
                data.get(
                    "sources",
                    [],
                ),
            )

        try:
            error = response.json().get(
                "detail",
                response.text,
            )
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

        response = requests.delete(
            f"{BACKEND_URL}/document/{document_id}",
            timeout=30,
        )

        return response.ok

    except requests.exceptions.RequestException:
        return False


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">

            <div class="brand-icon">
                ✦
            </div>

            <div class="brand-name">
                RAG Assistant
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "＋  New chat",
        use_container_width=True,
    ):

        create_new_chat()

        st.rerun()


    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-heading">Documents</div>',
        unsafe_allow_html=True,
    )


    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed",
    )


    if uploaded_file:

        st.markdown(
            f"""
            <div class="document-card">

                <div class="document-name">
                    📄 {html.escape(uploaded_file.name)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        if st.button(
            "Process document",
            use_container_width=True,
        ):

            with st.spinner("Processing document..."):

                success, result = upload_document(
                    uploaded_file
                )


            if success:

                st.success(
                    "Document processed successfully."
                )

                load_documents()

            else:

                st.error(str(result))


    # --------------------------------------------------------
    # DOCUMENT LIBRARY
    # --------------------------------------------------------

    load_documents()


    if st.session_state.documents:

        for document in st.session_state.documents:

            # Handle different possible response structures
            document_id = (
                document.get("document_id")
                or document.get("id")
            )

            filename = (
                document.get("filename")
                or document.get("name")
                or document.get("file_name")
                or "Document"
            )


            st.markdown(
                f"""
                <div class="document-card">

                    <div class="document-name">
                        📄 {html.escape(str(filename))}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


            if document_id:

                if st.button(
                    "Delete",
                    key=f"delete_{document_id}",
                    use_container_width=True,
                ):

                    if delete_document(document_id):

                        st.success("Document deleted.")

                        load_documents()

                        st.rerun()

                    else:

                        st.error(
                            "Could not delete document."
                        )


    # --------------------------------------------------------
    # SETTINGS
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-heading">Settings</div>',
        unsafe_allow_html=True,
    )


    st.session_state.show_sources = st.toggle(
        "Show sources",
        value=st.session_state.show_sources,
    )


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            position: fixed;
            bottom: 15px;
            color: #666;
            font-size: 11px;
        ">
            RAG Assistant · Local
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN
# ============================================================

st.markdown(
    '<div class="main-container">',
    unsafe_allow_html=True,
)


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome-container">

            <div class="welcome-icon">
                ✦
            </div>

            <div class="welcome-title">
                How can I help you?
            </div>

            <div class="welcome-subtitle">
                Ask questions about your uploaded documents.
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

        safe_content = html.escape(
            message["content"]
        )

        st.markdown(
            f"""
            <div class="message-row user">

                <div class="user-bubble">
                    {safe_content}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    else:

        st.markdown(
            f"""
            <div class="message-row assistant">

                <div class="assistant-wrapper">

                    <div class="assistant-avatar">
                        ✦
                    </div>

                    <div class="assistant-content">
                        {message["content"]}
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        # ----------------------------------------------------
        # SOURCES
        # ----------------------------------------------------

        sources = message.get(
            "sources",
            [],
        )


        if (
            st.session_state.show_sources
            and sources
        ):

            with st.expander(
                f"📚 Sources ({len(sources)})"
            ):

                for index, source in enumerate(
                    sources,
                    start=1,
                ):

                    source_text = (
                        source.get("text", "")
                        if isinstance(source, dict)
                        else str(source)
                    )

                    safe_source = html.escape(
                        source_text
                    )

                    st.markdown(
                        f"""
                        <div class="source-card">

                            <strong>
                                Source {index}
                            </strong>

                            <br><br>

                            {safe_source}

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Message RAG Assistant..."
)


if prompt:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )


    # --------------------------------------------------------
    # BACKEND
    # --------------------------------------------------------

    with st.spinner("Thinking..."):

        answer, sources = send_question(
            prompt
        )


    # --------------------------------------------------------
    # ASSISTANT MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )


    st.rerun()