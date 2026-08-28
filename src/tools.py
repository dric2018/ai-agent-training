import pickle
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.tools import tool

from config import CFG

# Chargement des instances persistées
embeddings = OpenAIEmbeddings(model=CFG.EMBEDDING_MODEL_NAME)

# Chargement ChromaDB
vectorstore = Chroma(
    persist_directory=CFG.DB_DIR, 
    embedding_function=embeddings
)
semantic_retriever = vectorstore.as_retriever(search_kwargs={"k": CFG.TOP_K})

# Chargement BM25
with open("bm25_index.pkl", "rb") as f:
    keyword_retriever = pickle.load(f)

keyword_retriever.k = CFG.TOP_K

# Création du moteur hybride
hybrid_retriever = EnsembleRetriever(
    retrievers=[semantic_retriever, keyword_retriever],
    weights=[0.7, 0.3]
)

@tool
def search_past_reviews(query: str, search_type:str="hybrid") -> str:
    """
    Effectue une recherche hybride (sémantique + mots-clés) dans la base 
    de données des avis clients passés d'Orange Côte d'Ivoire.

    search_type: soit "hybrid", "semantic", ou "keyword"
    """
    assert search_type in [ "hybrid", "semantic", "keyword"], f"Le type de recherche que vous voulez utiliser ({search_type}) n'est pas supporté"

    if search_type=="hybrid":
        docs = hybrid_retriever.invoke(query)
    elif search_type=="semantic":
        docs = semantic_retriever.invoke(query)
    else:
        docs = keyword_retriever.invoke(query)     

    res = []
    for d in docs:
        sentiment = d.metadata.get("sentiment", "N/A")
        res.append(f"[Sentiment: {sentiment}] Avis: {d.page_content}")
        
    return "\n\n".join(res) if res else "Aucun avis trouvé."