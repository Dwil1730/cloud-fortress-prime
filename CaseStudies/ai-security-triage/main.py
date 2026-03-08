from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
import pandas as pd

app = FastAPI(title="AI Security Triage Demo")

def guard_input(query: str):
    bad_words = ['ignore', 'rules', 'jailbreak', 'system prompt', 'password', 'admin', 'secret', 'override']
    for word in bad_words:
        if word in query.lower():
            return "Blocked: Adversarial prompt detected - potential jailbreak attempt"
    return query

df = pd.read_csv('clean_tickets.csv')
texts = df['text'].tolist()
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.create_documents(texts)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embeddings)
llm = Ollama(model="llama3.1:8b")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

class Incident(BaseModel):
    description: str

@app.post("/triage")
def triage(incident: Incident):
    guarded = guard_input(incident.description)
    if "Blocked" in guarded:
        return {"action": guarded, "confidence": 0.99}
    result = qa_chain({"query": guarded})
    return {
        "action": result['result'],
        "sources": [doc.page_content[:150] for doc in result['source_documents']],
        "confidence": 0.85
    }
