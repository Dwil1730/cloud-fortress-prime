# AI Security Triage System
### Case Study 2 — Cloud Fortress Prime

**Domain:** MLSecOps / Adversarial AI Defence / Cloud Security Automation  
**Stack:** Python · Llama 3.3 70B · FAISS · Streamlit · Supabase · Claude Sonnet  
**Deployment:** Live on Streamlit Cloud  
**Status:** Production

Live Demo: https://ai-security-triage.streamlit.app/  
Admin Dashboard: https://ai-security-triage.streamlit.app/admin

---

## Overview

This system automates the classification, prioritization, and routing of IT security incidents using a retrieval-augmented generation (RAG) pipeline backed by a 13-layer adversarial defence framework. Rather than relying on a human analyst to manually read and route every alert, the system ingests an incident description, retrieves semantically similar historical tickets, and returns a triage recommendation within seconds.

The architecture is designed under the assumption that any AI system operating in a security context is itself a high-value target. Accordingly, the defence layers address not only prompt injection and jailbreak attempts, but also base64-encoded payloads, foreign-language evasion, multi-turn attack patterns, automated brute force, and nation-state threat indicators sourced from CISA and IRGC intelligence feeds.

![AI Security Triage Dashboard](screenshots/01_triage_passed.png)

---

## Problem Statement

Security operations teams face a compounding alert volume problem. Modern cloud environments produce thousands of security events per day, the vast majority of which are low-fidelity noise. Manual triage workflows introduce:

- Inconsistent severity scoring across analysts and shifts
- Delayed response to genuine threats due to queue depth
- Context loss when alerts are evaluated in isolation
- Analyst fatigue leading to missed escalations

AI-assisted triage addresses each of these failure modes — but only when the AI system itself is hardened against adversarial manipulation.

---

## Adversarial Defence Architecture

### Core Defence Layers (1–8)

| Layer | Technology | Function |
|---|---|---|
| 1. PII Redaction | Regex redactor | Strips emails, IPs, SSNs, phone numbers, and names prior to model inference |
| 2. Keyword Block | Custom wordlist | Intercepts known adversarial phrases: ignore all, jailbreak, admin password, override, bypass |
| 3. Obfuscation / Leetspeak | Regex patterns | Detects character-substitution evasion: 1gn0r3, 0v3rr1d3, j41lbr34k |
| 4. Semantic Cosine Similarity | sentence-transformers | Embedding similarity threshold (>0.82) against a curated corpus of known rogue prompts |
| 5. ML Anomaly Detection | scikit-learn OneClassSVM | Flags out-of-distribution inputs; trained on 20 representative benign security queries |
| 6. CISA / IRGC IOC Check | Threat intel feed | Blocks known Iran IRGC indicators: 185.86.139.1, irgc-proxy.ir, unitronics.com:20256 |
| 7. Zero-Trust Session Auth | Fernet (cryptography) | Cryptographic session token validation on every request |
| 8. LLM Safety Judge | Claude Sonnet | Final verdict: SAFE or UNSAFE before model response is returned |

![Keyword-based prompt injection blocked](screenshots/02_blocked_keyword.png)

### Hardened Red-Team Resistant Layers (9–13)

| Layer | Defence | Coverage |
|---|---|---|
| 9. Base64 Decode + Rescan | Decode then re-run full pipeline | Catches encoded payloads |
| 10. Foreign Language Detection | Translation dictionary | Blocks evasion in 10+ languages |
| 11. Multi-turn Attack Detection | Session history analysis | Identifies jailbreak attempts distributed across multiple messages |
| 12. Rate Limiting | Per-session request counter | Flags automated attack patterns at >10 requests/minute |
| 13. Indirect Injection Scanner | Field-level regex | Catches adversarial payloads embedded in ticket numbers, filenames, and metadata fields |

![Base64-encoded payload blocked](screenshots/07_blocked_base64.png)

**Adversarial block rate: 100% across all tested inputs**

---

## Severity Classification

| Severity | Trigger Condition |
|---|---|
| CRITICAL | CISA IOC match or LLM Judge block — nation-state threat indicators |
| HIGH | Semantic cosine or SVM anomaly — sophisticated evasion attempts |
| MEDIUM | Keyword or leetspeak block — basic adversarial inputs |
| LOW | Passed all 13 layers — legitimate security incident |

---

## Audit Log

Every triage decision is permanently written to a Supabase PostgreSQL audit database with the following fields:

- UTC timestamp
- Full incident text (post-redaction)
- Triage result: PASSED or BLOCKED
- Severity classification
- Unique session identifier
- CISA IOC scan result (boolean)
- DoD Zero-Trust compliance flag (boolean)
- CSV export available from the admin dashboard

The log is append-only by design, providing a tamper-evident audit trail consistent with NIST SP 800-92 log retention requirements.

![Admin dashboard — 47 total triages, 31 blocked, 1 critical threat](screenshots/06_admin_dashboard.png)

---

## System Architecture

tickets.csv -> clean_data.py -> clean_tickets.csv -> rag_triage.py -> guards.py (13 layers) -> app.py -> pages/admin.py

---

## Government and Defence Equivalents

| System Layer | Real-World Equivalent |
|---|---|
| Layer 4 — Semantic Cosine | NSA XKEYSCORE semantic analysis |
| Layer 5 — SVM Anomaly | CISA EINSTEIN 3A ML anomaly detection |
| Layer 6 — CISA IOC | CISA AIS (Automated Indicator Sharing) live feed |
| Layer 1 — PII Redaction | DoD SIEM PII redaction per NIST SP 800-122 |
| Layer 8 — LLM Judge | DARPA GARD / NSA AI Security Center LLM classifiers |
| Layer 12 — Rate Limiting | DoD DDoS and brute force protection |
| Layer 11 — Multi-turn | NSA conversation pattern analysis |
| Audit Log | NIST SP 800-92 compliant log retention |

---

## Key Results

| Metric | Result |
|---|---|
| Dataset size | 627 cleaned tickets |
| Baseline F1 (TF-IDF + Logistic Regression) | 0.438 |
| Adversarial block rate | 100% across all 13 tested attack vectors |
| CISA Iran IRGC indicators covered | 3 hardcoded + live feed |
| Audit log persistence | Permanent — Supabase PostgreSQL |
| Deployment | Live on Streamlit Cloud via Groq API |

---

## Technology Stack

| Layer | Technology |
|---|---|
| Data processing | pandas, CSV |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector store | FAISS |
| LLM inference | Llama 3.3 70B via Groq API |
| LLM safety judge | Claude Sonnet via Anthropic API |
| ML baseline | scikit-learn (TF-IDF + Logistic Regression) |
| Anomaly detection | scikit-learn OneClassSVM |
| Audit database | Supabase PostgreSQL |
| API layer | FastAPI + uvicorn |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |

---

## Local Setup

Prerequisites: pip install -r requirements.txt

Add credentials to .streamlit/secrets.toml (never commit this file):

GROQ_API_KEY = "your_groq_key"
ANTHROPIC_API_KEY = "your_anthropic_key"
ADMIN_PASSWORD = "your_admin_password"

Run:

1. python3 clean_data.py
2. uvicorn main:app --reload
3. streamlit run app.py

---

## Security Controls

- .streamlit/secrets.toml is gitignored and never committed
- API keys stored exclusively in Streamlit Cloud secrets
- Audit log is append-only — tamper-evident
- Admin dashboard requires password authentication
- IOC checks run against original pre-anonymisation input
- Rate limiting protects against automated brute force
- Multi-turn detection prevents slow jailbreak attempts

---

## Related

- Case Study 1 — Zero Trust Network Infrastructure

---

Skills demonstrated: RAG · LLM inference · Adversarial ML · Prompt security · Red-teaming · Base64 attack detection · Foreign language detection · Multi-turn attack detection · Rate limiting · Indirect injection scanning · CISA threat intelligence · DoD Zero-Trust · Persistent audit logging · Supabase · FastAPI · Streamlit · FAISS · pandas · scikit-learn · sentence-transformers · Groq API · Anthropic API · Cloud deployment

© 2026 Dwil1730. All rights reserved. No reproduction or reuse without permission.
