import json
import os
import pickle
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

from config import CFG

from __init__ import logger

DATA_PATH = os.path.join(CFG.DATA_DIR, "data.jsonl")

def run_ingestion(
        data_path=DATA_PATH,
        db_dir=CFG.DB_DIR, 
        bm25_path="bm25_index.pkl"
    ):
    documents = []
    
    # Chargement du JSONL
    with open(data_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                text = data.pop("review_text", data.pop("text", ""))
                if text:
                    documents.append(Document(page_content=text, metadata=data))

    # Création et persistance ChromaDB
    embeddings = OpenAIEmbeddings(model=CFG.EMBEDDING_MODEL_NAME)

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=db_dir
    )
    logger.info(f"ChromaDB persisté dans {db_dir}")

    # Création et persistance BM25
    bm25_retriever = BM25Retriever.from_documents(documents)
    with open(bm25_path, "wb") as f:
        pickle.dump(bm25_retriever, f)

    logger.info(f"Index BM25 sauvegardé dans {bm25_path}")

if __name__ == "__main__":
    run_ingestion()