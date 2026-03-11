import streamlit as st
import json
import urllib.request
import pandas as pd
from datetime import datetime

SUPABASE_URL = "https://rlkbwlmyiimlbrkokyfb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsa2J3bG15aWltbGJya29reWZiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMyMDI1OTMsImV4cCI6MjA4ODc3ODU5M30.PdqMyWAS0DLP-c-rrRtDFoyg8AQzNpa_cRJXDihLEIE"

st.set_page_config(page_title="Admin Dashboard", layout="wide")

def load_all_entries():
    try:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/audit_log?order=timestamp.desc&limit=1000",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            }
        )
        response = urllib.request.urlopen(req)
        return json.loads(response.read())
    except Exception as e:
        return []

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.title("🔐 Admin Login")
    st.write("This area is restricted to authorized personnel only.")
    password = st.text_input("Enter Admin Password:", type="password")
    if st.button("Login"):
        try:
            correct = st.secrets["ADMIN_PASSWORD"]
        except:
            correct = "Cobssuutt!36"
        if password == correct:
            st.session_state.admin_authenticated = True
            st.rerun()
        else:
            st.error("Access denied.")
else:
    st.title("🛡️ DoD Security Triage — Admin Dashboard")
    st.success("Authenticated — Welcome, Administrator")
    if st.button("Logout"):
        st.session_state.admin_authenticated = False
        st.rerun()
    st.markdown("---")
    entries = load_all_entries()
    if entries:
        df = pd.DataFrame(entries)
        df["timestamp"] = df["timestamp"].str[:16].str.replace("T", " ")
        df["incident"] = df["incident"].str[:80]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Triages", len(df))
        col2.metric("Blocked", len(df[df["result"] == "BLOCKED"]))
        col3.metric("Passed", len(df[df["result"] == "PASSED"]))
        col4.metric("Critical Threats", len(df[df["severity"] == "CRITICAL"]))
        st.markdown("---")
        st.markdown("### 🔴 Blocked Threats")
        blocked = df[df["result"] == "BLOCKED"][["timestamp","incident","reason","severity","session_id"]]
        st.dataframe(blocked, use_container_width=True)
        st.markdown("### 🟢 Passed Incidents")
        passed = df[df["result"] == "PASSED"][["timestamp","incident","reason","severity","session_id"]]
        st.dataframe(passed, use_container_width=True)
        st.markdown("### 📊 Full Audit Log")
        st.dataframe(df[["timestamp","incident","result","reason","severity","session_id"]], use_container_width=True)
        csv = df.to_csv(index=False)
        st.download_button("Download Full Audit Log CSV", csv, "audit_log.csv", "text/csv")
    else:
        st.warning("No audit entries found.")
