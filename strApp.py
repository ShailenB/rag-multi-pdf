import streamlit as st
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA

load_dotenv()
st.set_page_config(
    page_title="Multi-PDF RAG Chatbot",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
    }
    .block-container {
        padding-top: 2rem;
        max-width: 1100px;
    }
    h1 {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: #1e293b !important;
        text-align: center;
        margin-bottom: 1rem;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid #e2e8f0;
    }
    .stChatMessage {
        border-radius: 18px;
        padding: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 10px;
        background: white;
    }
    .stTextInput input, .stChatInput input {
        border-radius: 14px !important;
        border: 1px solid #cbd5e1 !important;
        padding: 12px !important;
    }
    .pdf-card {
        background: white;
        padding: 16px;
        border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 18px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>📘 Multi-PDF RAG Chatbot</h1>", unsafe_allow_html=True)
st.caption("Ask questions across your selected knowledge base with grounded answers and source pages")

model = "meta-llama/llama-4-scout-17b-16e-instruct"

# Sidebar PDF selector
available_pdfs = [
    folder for folder in os.listdir("vector_db")
    if os.path.isdir(
        os.path.join("vector_db", folder)
    )
]

with st.sidebar:
    st.markdown("## 📚 Knowledge Base")
    st.caption("Semantic document assistant")

    st.markdown(
        """
        <div style="
            background: white;
            padding: 14px;
            border-radius: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: 12px;
        ">
            <b>📄 Active Source</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_pdf = st.selectbox(
        "",
        available_pdfs
    )

    st.markdown("---")

@st.cache_resource
def load_vector_store(pdf_name):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db_path = os.path.join(
        "vector_db",
        pdf_name
    )

    vector_store = FAISS.load_local(
        db_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store


if "msg" not in st.session_state:
    st.session_state.msg = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []



for message in st.session_state.msg:
    st.chat_message(message["role"]).markdown(
        message["content"]
    )

prompt = st.chat_input("Ask a question")

if prompt:
    st.chat_message("user").markdown(prompt)

    st.session_state.msg.append(
        {"role": "user", "content": prompt}
    )
    st.session_state.chat_history.append(
        {"role": "user", "content": prompt}
    )


    groq_chat = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name=model
    )

    vector_store = load_vector_store(
        selected_pdf
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 5}
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=groq_chat,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )
    history_context = "\n".join(
        [f"{item['role']}: {item['content']}" for item in st.session_state.chat_history[-6:]]
    )



    full_query = f"""
    Use the conversation history and context to answer.

    Conversation:
    {history_context}

    Current question:
    {prompt}
    """

    result = qa_chain.invoke(
        {"query": full_query}
    )

    response = result["result"]

    st.chat_message("assistant").markdown(
        response
    )

    st.session_state.msg.append(
        {
            "role": "assistant",
            "content": response
        }
    )
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response}
    )


    with st.expander("Sources"):
        for doc in result[
            "source_documents"
        ]:
            st.markdown(
                f"**Page {doc.metadata.get('page')}**"
            )
            st.write(
                doc.page_content[:500]
            )