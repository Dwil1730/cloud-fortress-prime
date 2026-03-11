import os
import asyncio
import json
import uuid
from datetime import datetime, timezone
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_text_splitters import CharacterTextSplitter
import pandas as pd
from guards import battle_guard

st.set_page_config(page_title="🛡️ AI Security Triage", layout="wide")

SUPABASE_URL = "https://rlkbwlmyiimlbrkokyfb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsa2J3bG15aWltbGJya29reWZiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMyMDI1OTMsImV4cCI6MjA4ODc3ODU5M30.PdqMyWAS0DLP-c-rrRtDFoyg8AQzNpa_cRJXDihLEIE"

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

def get_severity(verdict, reason):
    if verdict == "BLOCKED":
        if "CISA IOC" in reason or "LLM Judge" in reason:
            return "CRITICAL"
        if "Semantic" in reason or "Anomaly" in reason:
            return "HIGH"
        return "MEDIUM"
    return "LOW"

def save_to_supabase(incident, verdict, reason, severity):
    try:
        import urllib.request
        data = json.dumps({
            "incident": incident[:200],
            "result": verdict,
            "reason": reason,
            "severity": severity,
            "session_id": st.session_state.session_id,
            "cisa_ioc_scanned": True,
            "dod_zt_compliance": True
        }).encode()
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/audit_log",
            data=data,
            headers={
                "Content-Type": "application/json",
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Prefer": "return=minimal"
            },
            method="POST"
        )
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Supabase error: {e}")
        return False

def load_from_supabase():
    try:
        import urllib.request
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/audit_log?order=timestamp.desc&limit=10",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            }
        )
        response = urllib.request.urlopen(req)
        return json.loads(response.read())
    except Exception as e:
        print(f"Supabase load error: {e}")
        return []

with st.sidebar:
    st.markdown("## 🔒 Active Defence Layers")
    st.markdown("""
    1. 🧹 **PII Redaction** — Regex redactor
    2. 🚫 **Keyword Block** — Adversarial phrases
    3. 🔤 **Obfuscation/Leetspeak** — Regex patterns
    4. 🧠 **Semantic Cosine** — Rogue similarity >0.82
    5. 🤖 **ML Anomaly SVM** — OneClassSVM outlier
    6. 🌐 **CISA IOC Check** — Known threat indicators
    7. 🔐 **DoD Zero-Trust Auth** — Token validation
    8. ⚖️ **Claude LLM Judge** — Final safety verdict
    """)
    st.markdown("---")
    st.markdown("### 📋 Live Audit Log")
    entries = load_from_supabase()
    if entries:
        for entry in entries:
            color = "🔴" if entry["result"] == "BLOCKED" else "🟢"
            ts = entry.get("timestamp", "")[:16].replace("T", " ")
            sev = entry.get("severity", "LOW")
            st.write(f"{color} `{entry['result']}` — {entry['reason'][:40]}")
            st.caption(f"🕐 {ts} UTC | ⚠️ {sev} | 🔑 {entry.get('session_id','?')}")
    else:
        st.write("No audit entries yet.")
    st.markdown(f"**Session ID:** `{st.session_state.session_id}`")

st.title("🛡️ AI Security Triage Demo")
st.write("Enter an incident description. **8-layer DoD/CISA defence** runs automatically.")

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
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents(texts)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)
    return RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )

qa_chain = load_chain()
description = st.text_input("🔍 Incident Description:", "phishing email alert from suspicious IP")

if st.button("🛡️ Run Triage"):
    with st.spinner("Running 8-layer defence gauntlet..."):
        verdict, reason = asyncio.run(battle_guard(description))

    severity = get_severity(verdict, reason)
    save_to_supabase(description, verdict, reason, severity)
    st.session_state.audit_log.append({"result": verdict, "reason": reason, "severity": severity})

    if verdict == "BLOCKED":
        st.error(f"🚫 BLOCKED — {reason}")
        st.warning(f"⚠️ Severity: **{severity}** | Logged to DoD audit database.")
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

    st.markdown("---")
    st.markdown("### 📊 Full Persistent Audit Log")
    all_entries = load_from_supabase()
    if all_entries:
        df_audit = pd.DataFrame(all_entries)[["timestamp","incident","result","reason","severity","session_id"]]
        df_audit["timestamp"] = df_audit["timestamp"].str[:16].str.replace("T"," ")
        df_audit["incident"] = df_audit["incident"].str[:50]
        st.dataframe(df_audit, use_container_width=True)
        csv = df_audit.to_csv(index=False)
        st.download_button("⬇️ Download Full Audit Log (CSV)", csv, "audit_log.csv", "text/csv")

    st.rerun()
