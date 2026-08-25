from __init__ import logger
from config import CFG

from langchain_core.messages import HumanMessage, AIMessage

import streamlit as st

from utils import render_agent_response

from time import time

agent = NotImplementedError


def query_llm(input_text: str):

    # current_history = st.session_state.get("messages", [])
    final_answer = None

    # User Message
    with st.chat_message("user"):
        st.markdown(input_text)
        st.session_state.messages.append(HumanMessage(content=input_text))

    # Assistant Message
    with st.chat_message("assistant"):
        with st.status("🔍 Thinking...", expanded=True) as status:
            start = time()
            for update in agent.get_answer(user_prompt=input_text):
                if update["type"] == "status":
                    action_present = True if "action" in update.keys() else False
                    if action_present:
                        pass
                    new_label = f"{update['content']}"
                    status.update(label=new_label, state="running", expanded=False)
                    status.write(f"⚙️ {new_label}")                    
                
                elif update["type"] in ["text", "data", "final"]:                    
                    final_answer = update
                       
                    duration = (time() - start) /60                        
                    status.update(
                        label=f"✅ Traitement terminé (en {duration:.3f} min)", 
                        state="complete", 
                        expanded=False
                    )
                    
                elif update["type"] == "error":
                    status.update(label="❌ Erreur de traitement ou requête bloquée", state="error")
                    final_answer = update

        if final_answer:
            with st.spinner(text="Préparation de la réponse finale...", show_time=True):
                render_agent_response(final_answer)

            st.session_state.messages.append(
                AIMessage(
                    content=final_answer.get("content", ""), 
                    additional_kwargs={
                        "full_response": final_answer,                     
                        "action": final_answer.get("action", "")
}
                )
            )

def select_suggestion():
    if st.session_state.suggestion_box:
        st.session_state.chat_input_key = st.session_state.suggestion_box

st.title("📄 OCI AI Agent")
st.markdown(
    "Bonjour! Bienvenue dans ce séminaire de formation. " \
    "Demande moi ce que tu veux...ou presque")

# Example suggestions
SUGGESTIONS = ["Qui es-tu?", "Qu'est-ce qu'un agent IA?"]

# Show only before the first message
if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = []

selected_option = st.pills(
    label="Examples:", 
    options=SUGGESTIONS,
    key="suggestion_box",
    on_change=select_suggestion,
    selection_mode="single"
)

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    
    elif isinstance(message, AIMessage):
        action = message.additional_kwargs.get("action")
        full_response = message.additional_kwargs.get("full_response")

        if action == "skip":
            logger.info("Skipping AI message rendering.")
            continue

        with st.chat_message("assistant"):
            if full_response and not action:
                render_agent_response(full_response)
            else:
                st.markdown(message.content)


chat_prompt = st.chat_input("Saisissez votre requête ici...", key="chat_input_key")


if chat_prompt:
    query_llm(input_text=chat_prompt)
