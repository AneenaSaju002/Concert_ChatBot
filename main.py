import streamlit as st
from langchain_helper import get_qa_chain, create_vector_db
import os

st.set_page_config(
    page_title="Candlelight Concert AI Assistant",
    page_icon="🕯️",
    layout="centered"
)


st.markdown("""
    <style>
    :root {
        --gold: #C5A267;
        --dark: #000000;
        --darker: #0A0A0A;
    }

    body {
        color: white;
        background-color: var(--dark);
    }

    .stApp {
        background: linear-gradient(to bottom, #000000, #1a1a1a);
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--gold) !important;
    }

    .stTextInput>div>div>input {
        color: white !important;
        background-color: var(--darker) !important;
        border: 1px solid var(--gold) !important;
    }

    .stButton>button {
        background-color: var(--gold) !important;
        color: black !important;
        border: none !important;
        font-weight: bold;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background-color: #D6B77E !important;
        transform: scale(1.05);
    }

    .stExpander {
        background-color: var(--darker);
        border: 1px solid var(--gold) !important;
    }

    .stExpander .stMarkdown {
        color: white !important;
    }

    .gold-text {
        color: var(--gold) !important;
        font-weight: bold;
    }

    .chat-history {
        border-left: 3px solid var(--gold);
        padding-left: 1rem;
        margin: 1.5rem 0;
    }

    .image-row {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 30px;
    }

    .image-container {
        flex: 1;
        max-width: 30%;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    }

    .sidebar-section {
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Candlelight Concert AI Assistant")
st.subheader("Ask anything about our concerts, venues, or tickets")


with st.sidebar:
    st.image("img3.jpg", use_column_width=True)

    with st.container():
        st.header("About Candlelight")
        st.write(
            "Experience classical music in a new light with our mesmerizing candlelit performances in extraordinary venues.")

    with st.container():
        st.subheader("Contact")
        st.markdown("""
        📞 Box Office: (555) 123-4567
        ✉️ info@candlelightconcerts.com
        📍 123 Symphony Lane, Music City
        """)


main_container = st.container()

with main_container:

    index_exists = os.path.exists("faiss_index/index.faiss")

    with st.expander("🔍 Knowledge Base Setup", expanded=not index_exists):
        if not index_exists:
            st.warning("Knowledge base not initialized")
            if st.button("Build Concert Knowledge Base", key="create_db"):
                with st.spinner("Creating knowledge base... (This may take several minutes)"):
                    create_vector_db()
                    st.success("Knowledge base created successfully!")
                    st.experimental_rerun()
        else:
            st.success("Concert knowledge base is ready")
            if st.button("Rebuild Knowledge Base", key="rebuild_db"):
                with st.spinner("Recreating knowledge base..."):
                    create_vector_db()
                    st.success("Knowledge base updated successfully!")
                    st.experimental_rerun()


    question = st.text_input("Ask your question about Candlelight Concerts:",
                             placeholder="e.g., What's the dress code? Can I bring children?")

    if question:
        if not index_exists:
            st.warning("Please build the knowledge base first")
        else:
            chain = get_qa_chain()
            inputs = {
                "question": question,
                "chat_history": st.session_state.chat_history
            }

            with st.spinner("Finding the best answer for you..."):
                response = chain(inputs)
                answer = response["answer"]

                # Display response
                st.subheader("Answer")
                st.markdown(f'<div class="chat-history">{answer}</div>', unsafe_allow_html=True)

                # Update chat history
                st.session_state.chat_history.append((question, answer))


    if st.session_state.chat_history:
        with st.expander("💬 Conversation History", expanded=True):
            for i, (q, a) in enumerate(st.session_state.chat_history, 1):
                st.markdown(f'<p class="gold-text">Q{i}: {q}</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-history">A{i}: {a}</div>', unsafe_allow_html=True)


st.markdown('<div class="image-row">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image("img1.jpg", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image("img5.jpg", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image("img4.jpg", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

