import streamlit as st 
from src import logger
import re
from src.config import CFG

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def parse_thinking_stream(stream):
    thinking_expander = st.expander("Show Reasoning", expanded=True)
    thinking_container = thinking_expander.empty()
    response_container = st.empty()

    full_thinking = ""
    full_response = ""
    is_thinking = False

    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        
        if "<think>" in content:
            is_thinking = True
            content = content.replace("<think>", "")
            
        if "</think>" in content:
            is_thinking = False
            content = content.replace("</think>", "")

        if is_thinking:
            full_thinking += content
            thinking_container.markdown(full_thinking)
        else:
            full_response += content
            response_container.markdown(full_response)
            
    return full_thinking, full_response


def calc_similarity(text1, text2):
    # Vectorize the text documents
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Compute cosine similarity between the first and second vector
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    score = similarity[0][0]
    print(f"TF-IDF Cosine Similarity: {similarity[0][0]:.4f}")

    return score
