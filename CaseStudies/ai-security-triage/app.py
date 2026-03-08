import streamlit as st
import requests

st.title("AI Security Triage Demo")
st.write("Enter incident description. Guards block attacks.")

description = st.text_input("Incident:", "phishing email alert")

if st.button("Triage"):
    response = requests.post(
        "http://127.0.0.1:8000/triage",
        json={"description": description}
    )
    if response.status_code == 200:
        result = response.json()
        st.success("Recommended Action:")
        st.write(result['action'])
        st.write("Confidence:", result['confidence'])
        if "sources" in result:
            st.write("Sources:")
            for src in result['sources']:
                st.write(f"- {src}")
    else:
        st.error("API error — is uvicorn running?")
