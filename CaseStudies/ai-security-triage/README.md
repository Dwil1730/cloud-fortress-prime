# AI Security Triage (Case Study 2)

Secure RAG-based triage for cyber incidents — built locally on M1 Mac.  
Extends CaseStudy1 Zero Trust infra to **AI prompt security**.

## Key Results
- Cleaned 627 real tickets (pandas)  
- Baseline: TF-IDF + Logistic Regression → F1 0.438  
- RAG: FAISS + Llama 3.1 8B → recommendations + sources  
- Guards: Blocked prompt injections → **100% success**  
- Deploy: FastAPI API + Streamlit dashboard  

## Proof (Screenshots)
! (screenshots/01-folder-overview.png) - Project overview  
! (screenshots/02-cleaning-script.png) - Data cleaning  
! (screenshots/03-cleaned-627-rows.png) - 627 rows ready  
! (screenshots/04-baseline-f1.png) - Baseline F1  
! (screenshots/05-rag-guards-blocked.png) - RAG + attack block  
! (screenshots/06-ollama-running.png) - Ollama running  
! (screenshots/07-guard-function.png) - Guard code  
! (screenshots/08-git-status.png) - Git status  
! (screenshots/09-dashboard-demo.png) - Dashboard normal  
! (screenshots/10-dashboard-blocked.png) - Dashboard blocked  

## Run
1. `ollama serve &`  
2. `uvicorn main:app --reload`  
3. `streamlit run app.py`  

Skills: RAG, LLM inference, prompt security, red-teaming, FastAPI, Streamlit, Git, pandas.  
Ready for AI Security Engineer roles (Perplexity, VA EHRM).
