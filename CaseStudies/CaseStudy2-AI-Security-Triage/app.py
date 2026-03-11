import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_text_splitters import CharacterTextSplitter
import pandas as pd

st.title("🛡️ AI Security Triage Demo")
st.write("Enter an incident description. Adversarial inputs are blocked automatically.")

def guard_input(query: str) -> str:
    bad_words = ["ignore", "rules", "jailbreak", "system prompt", "password", "admin", "secret", "override"]
    for word in bad_words:
        if word in query.lower():
            return "Blocked: Adversarial prompt detected - potential jailbreak attempt"
    return query

@st.cache_resource
def load_chain():
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not found.")
        st.stop()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "clean_tickets.csv")
    df = pd.read_csv(csv_path)
    texts = df["text"].tolist()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents(texts)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever(search_kwargs={"k": 3}), return_source_documents=True)

qa_chain = load_chain()
description = st.text_input("Incident:", "phishing email alert")
if st.button("Triage"):
    guarded = guard_input(description)
    if "Blocked" in guarded:
        st.error(f"🚫 {guarded}")
    else:
        result = qa_chain.invoke({"query": guarded})
        st.success("✅ Recommended Action:")
        st.write(result["result"])
        if result.get("source_documents"):
            st.write("**Sources:**")
            for doc in result["source_documents"]:
                st.write(f"- {doc.page_content[:150]}")
