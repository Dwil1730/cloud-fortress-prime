import os
import asyncio
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_text_splitters import CharacterTextSplitter
import pandas as pd
import json
from guards import battle_guard

st.set_page_config(page_title="🛡️ AI Security Triage", layout="wide")
st.title("🛡️ AI Security Triage Demo")
st.write("Enter an incident description. **8-layer DoD/CISA defence** runs automatically.")

with st.sidebar:
    st.markdown("## 🔒 Active Defence Layers")
    st.markdown("""
    1. 🧹 **PII Redaction** — Presidio anonymizer
    2. 🚫 **Keyword Block** — Adversarial phrases
    3. 🔤 **Obfuscation/Leetspeak** — Regex patterns
    4. 🧠 **Semantic Cosine** — Rogue similarity >0.82
    5. 🤖 **ML Anomaly SVM** — OneClassSVM outlier
    6. 🌐 **CISA IOC Check** — Known threat indicators
    7. 🔐 **DoD Zero-Trust Auth** — Token validation
    8. ⚖️ **Claude LLM Judge** — Final safety verdict
    """)
    st.markdown("---")
    st.markdown("### 📋 Last 5 Audit Entries")
    if os.path.exists("audit_trail.jsonl"):
        with open("audit_trail.jsonl") as f:
            lines = f.readlines()[-5:]
        for line in lines:
            entry = json.loads(line)
            color = "🔴" if entry["guard_result"] == "BLOCKED" else "🟢"
            st.write(f"{color} `{entry['guard_result']}` — {entry['reason'][:50]}")
    else:
        st.write("No audit entries yet.")

@st.cache_resource
def load_chain():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except:
            st.error("GROQ_API_KEY not found.")
            st.stop()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "clean_tickets.csv")
    df = pd.read_csv(csv_path)
    texts = df["text"].tolist()
    splitter = __import__("langchain_text_splitters").CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents(texts)
    embeddings = __import__("langchain_community.embeddings", fromlist=["HuggingFaceEmbeddings"]).HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = __import__("langchain_community.vectorstores", fromlist=["FAISS"]).FAISS.from_documents(docs, embeddings)
    llm = __import__("langchain_groq", fromlist=["ChatGroq"]).ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)
    return __import__("langchain_classic.chains", fromlist=["RetrievalQA"]).RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )

qa_chain = load_chain()
description = st.text_input("🔍 Incident Description:", "phishing email alert from suspicious IP")

if st.button("🛡️ Run Triage"):
    with st.spinner("Running 8-layer defence gauntlet..."):
        verdict, reason = asyncio.run(battle_guard(description))
    if verdict == "BLOCKED":
        st.error(f"🚫 BLOCKED — {reason}")
        st.warning("Input flagged and logged to audit trail.")
    else:
        st.success(f"✅ PASSED all 8 layers — {reason}")
        with st.spinner("Querying RAG chain..."):
            result = qa_chain.invoke({"query": description})
        st.markdown("### 📌 Recommended Action")
        st.write(result["result"])
        if result.get("source_documents"):
            with st.expander("📂 Source Tickets Used"):
                for doc in result["source_documents"]:
                    st.write(f"- {doc.page_content[:200]}")
