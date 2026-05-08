# AI Security Triage System

### Cloud Fortress Prime — Case Study 2

**Domain:** Security Engineering / SOC Workflow Automation / AI-Assisted Alert Classification / Adversarial Input Testing
**Stack:** Python · Llama 3.3 70B · FAISS · Streamlit · Supabase · Claude Sonnet (evaluation layer)
**Deployment:** Streamlit Cloud (Prototype / Engineering Demo)
**Status:** Experimental System (Non-Production)

Live Demo: [https://ai-security-triage.streamlit.app/](https://ai-security-triage.streamlit.app/)
Admin Dashboard: [https://ai-security-triage.streamlit.app/admin](https://ai-security-triage.streamlit.app/admin)

---

## Overview

This project is a **security engineering prototype** designed to explore how AI-assisted systems can support SOC-style alert triage workflows.

It combines:

* rule-based filtering
* embedding-based similarity search (FAISS)
* lightweight ML anomaly detection
* LLM-assisted classification (assistive role)

The system is intended for **engineering evaluation and workflow experimentation**, not production deployment.

---

## Problem Statement

Security teams face:

* High alert volume from cloud environments
* Inconsistent manual triage decisions
* Alert fatigue impacting prioritization quality
* Limited automation in early-stage alert filtering

This project explores whether layered automation techniques can improve consistency and reduce manual triage effort in a controlled environment.

---

## Scope & Limitations

This system is:

* a prototype built for engineering exploration
* not production validated
* not a certified security control system
* not a replacement for human SOC analysts

### Limitations:

* synthetic and sample data used (not enterprise SOC traffic)
* results are indicative, not production benchmarks
* LLM outputs are probabilistic and not deterministic
* detection performance depends on input distribution

---

## System Architecture

```text
Input Alert
   ↓
Preprocessing (cleaning / normalization)
   ↓
Rule-Based Filtering (keywords + heuristics)
   ↓
Embedding Similarity Search (FAISS)
   ↓
ML Layer (anomaly detection)
   ↓
LLM Classification (assistive only)
   ↓
Output: severity classification
   ↓
Audit Logging (Supabase PostgreSQL)
```

---

## Key Capabilities

* classifies incoming security-like alerts into severity levels
* applies rule-based filtering for known patterns
* uses embeddings for semantic similarity matching
* applies lightweight anomaly detection for outlier detection
* logs all decisions for traceability and debugging

---

## Adversarial Input Testing (Engineering Evaluation)

The system was tested against controlled adversarial-style inputs:

### 1. Prompt Injection Attempts

* instructions embedded in alert payloads
* attempts to override classification behavior

Result:

* rule-based filtering mitigates simple cases
* LLM remains assistive and does not control final logic

---

### 2. Obfuscated Inputs

* base64 encoded payloads
* leetspeak and character substitution
* unicode variations

Result:

* preprocessing improves visibility of encoded inputs
* advanced obfuscation remains a known limitation

---

### 3. Multi-Step Manipulation

* context drift across multiple inputs
* gradual instruction manipulation attempts

Result:

* partial detection via session tracking
* LLM context limitations acknowledged

---

## Evaluation Notes

This system was evaluated using:

* synthetic alert datasets
* rule-generated test cases
* adversarial-style input variations
* controlled simulation scenarios

### Important:

* no production SOC dataset used
* results are not statistically benchmarked at enterprise scale
* system behavior is dependent on input quality and distribution

---

## Audit Logging

All outputs are stored in Supabase PostgreSQL for traceability.

Each record includes:

* timestamp
* processed input (post-cleaning)
* classification output
* severity label
* decision path (rule / ML / LLM)

---

## Severity Classification

| Level    | Meaning                                   |
| -------- | ----------------------------------------- |
| Critical | High-confidence security-relevant pattern |
| High     | Suspicious or anomalous behavior          |
| Medium   | Requires analyst review                   |
| Low      | Likely benign or informational            |

---

## Technology Stack

* Python
* Streamlit
* FAISS
* scikit-learn
* Sentence Transformers
* Llama 3.3 70B (API)
* Claude Sonnet (evaluation layer)
* Supabase (PostgreSQL)

---

## Screenshots

<img src="screenshots/01_triage_passed.png" width="600"/>
<img src="screenshots/02_blocked_keyword.png" width="600"/>
<img src="screenshots/06_admin_dashboard.png" width="600"/>
<img src="screenshots/07_blocked_base64.png" width="600"/>

---

## Key Engineering Takeaways

This project demonstrates:

* layered security engineering design
* tradeoffs between rule-based, ML, and LLM systems
* limitations of probabilistic models in security workflows
* importance of audit logging and traceability
* early-stage SOC automation concepts

---

## Final Classification

This project is a:

> **security engineering prototype for SOC workflow experimentation**

It is NOT:

* a production SOC system
* a certified security control framework
* or a deterministic detection engine

---

## Skills Demonstrated

SOC workflow design · security engineering · anomaly detection concepts · embedding-based retrieval · LLM integration patterns · audit logging design · adversarial input testing · cloud deployment basics

---

