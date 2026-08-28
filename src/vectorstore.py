import json
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Chroma

from tqdm import tqdm

import os
import streamlit as st

from config import CFG

def load_jsonl_to_docs(file_path: str) -> list[Document]:
  documents = []
  with open(file_path, "r", encoding="utf-8") as f:
    for line in tqdm(f):
      if line.strip():
        data = json.loads(line)

        # On extrait le texte de l'avis (adaptez la clé selon votre JSONL, ex: "review_text" ou "text")
        text = data.get("review_text", data.get("text", ""))

        # Tout le reste devient les métadonnées (sentiment, id, date, etc.)
        metadata = {
            k: v for k, v in data.items() if k not in ["review_text", "text"]
        }

        if text:
          documents.append(Document(page_content=text, metadata=metadata))
  return documents


@st.cache_resource
def init_vectorstore(search_type:str):
  """Charge le dataset .jsonl et initialise ChromaDB pour le RAG."""
  jsonl_path = "french_customer_reviews.jsonl"

  # Fallback de secours si le fichier n'existe pas encore pour les tests
  if not os.path.exists(jsonl_path):
    os.makedirs("data", exist_ok=True)
    with open(jsonl_path, "w", encoding="utf-8") as f:
      f.write(
          '{"review_id": 1, "sentiment": "negatif", "review_text": "Coupure de'
          ' fibre récurrente à Cocody ce mois-ci."}\n'
      )
      f.write(
          '{"review_id": 2, "sentiment": "positif", "review_text": "Très bon'
          ' service client en agence."}\n'
      )

  # Chargement direct des documents depuis le JSONL
  docs = load_jsonl_to_docs(jsonl_path)

  embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
  vectorstore = Chroma.from_documents(docs, embeddings)

  return vectorstore.as_retriever(
      search_kwargs={"k": CFG.NUM_RAG_DOCS}
  )  # Récupère les 2 avis les plus pertinents


__all__ = ["vectorstore", "docs", "embeddings"]
