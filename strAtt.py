# Add this near the top of your Streamlit app (after imports)
import streamlit as st


# Replace title section with this
st.markdown("<h1>📘 Multi-PDF RAG Chatbot</h1>", unsafe_allow_html=True)
st.caption("Ask questions across your selected knowledge base with grounded answers and source pages")

# Sidebar enhancement
with st.sidebar:
    st.markdown("### 📚 Knowledge Base")
    st.markdown("Select a PDF to chat with")

# Optional welcome card for main page
st.markdown(
    """
    <div class='pdf-card'>
        <b>✨ Smart Features</b><br>
        • Semantic search across PDFs<br>
        • Source page references<br>
        • Fast Groq-powered answers<br>
        • Multi-document selection ready
    </div>
    """,
    unsafe_allow_html=True
)
