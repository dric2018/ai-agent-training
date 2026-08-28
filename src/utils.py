
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import random

def generate_random_session_name():
    # Listes de mots pour générer des noms de sessions thématiques et sympas
    adjectifs = [
        "Alpha",
        "Beta",
        "Optima",
        "Nova",
        "Nexus",
        "Quantum",
        "Apex",
        "Sigma",
    ]
    domaines = ["Réseau", "Facturation", "Support", "Fibre", "Mobile", "Client"]
    suffixes = ["Express", "Voice", "Insight", "Analytics", "Pro"]

    return f"{random.choice(adjectifs)}-{random.choice(domaines)}-{random.choice(suffixes)}"

def calc_similarity(text1, text2):
    # Vectorize the text documents
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Compute cosine similarity between the first and second vector
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    score = similarity[0][0]
    print(f"TF-IDF Cosine Similarity: {similarity[0][0]:.4f}")

    return score
