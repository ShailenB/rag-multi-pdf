# 📘 Multi-PDF RAG Chatbot

A **Retrieval-Augmented Generation (RAG)** based chatbot built with **Streamlit + LangChain + FAISS**, designed to answer questions from multiple PDFs with **grounded, source-backed responses**.

---

## 🚀 Features

* 📄 **Multi-PDF Support** – Select and query different textbooks
* 🔍 **Semantic Search (FAISS)** – Accurate retrieval using embeddings
* 💬 **Conversational Interface** – Chat-style interaction with history
* 🧠 **Query Rewriting** – Converts follow-up questions into standalone queries
* 📚 **Source Attribution** – Displays page references for answers
* ⚡ **Fast Inference** – Powered by Groq LLM (LLaMA-based models)

---

## 🏗️ Architecture

```text
User Query
   ↓
Query Rewriting (LLM)
   ↓
Vector Search (FAISS + Embeddings)
   ↓
Relevant Chunks Retrieved
   ↓
LLM Answer Generation (Grounded)
   ↓
Response + Source Documents
```

---

## 🧰 Tech Stack

* **Frontend:** Streamlit
* **LLM:** Groq (`ChatGroq`)
* **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
* **Vector DB:** FAISS
* **Framework:** LangChain

---

## 📂 Project Structure

```
CleanProject/
│
├── strApp.py              # Main Streamlit app
├── vector_db/             # Preprocessed FAISS vector stores (per PDF)
│   ├── book1/
│   ├── book2/
│
├── .env                   # API keys
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/multi-pdf-rag-chatbot.git
cd multi-pdf-rag-chatbot
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Mac/Linux
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

### 5️⃣ Run the app

```bash
streamlit run strApp.py
```

---

## 📊 How It Works

1. User selects a PDF from the sidebar
2. User asks a question
3. System:

   * Rewrites the query (for clarity)
   * Retrieves relevant chunks using FAISS
   * Generates an answer using LLM
4. Sources are displayed with page numbers

---

## 🧠 Key Design Decisions

### ✅ Query Rewriting

Improves retrieval accuracy by converting conversational queries into standalone queries.

### ✅ Strict Grounding

The system prioritizes retrieved context over LLM memory to reduce hallucinations.

### ✅ Separation of Concerns

* Query rewriting → LLM
* Retrieval → FAISS
* Answering → QA chain

---

## ⚠️ Limitations

* Depends on quality of PDF preprocessing
* Large PDFs may increase retrieval latency
* LLM may still hallucinate if retrieval fails (mitigated with safeguards)

---

## 🔮 Future Improvements

* 🔁 Hybrid Search (BM25 + Vector)
* 📌 Citation per sentence
* 🧮 Confidence scoring for answers
* 🧠 Reranking models for better retrieval
* 🌐 Deployment (Streamlit Cloud / Docker)

---

## 🖼️ Demo (Optional)

*Add screenshots or GIFs here*

---

## 🤝 Contributing

Contributions are welcome!
Feel free to open issues or submit pull requests.

---

## 📜 License

MIT License

---

## 👤 Author

**Shailendra Baraniya**

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!

