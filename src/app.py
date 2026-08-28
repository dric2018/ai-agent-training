import streamlit as st
from langchain_core.messages import HumanMessage

from agent import init_agent
from vectorstore import init_vectorstore


st.set_page_config(
    page_title="OCI Voice - Copilote Avis Clients", page_icon="🧡", layout="wide"
)

st.title("🧡 OCI Voice : Assistant d'Analyse des Avis Clients")
st.markdown(
    "Dataset : *French Customer Review Sentiment* | Orange Côte d'Ivoire"
)

retriever = init_vectorstore()
# initialize agent
agent_executor = init_agent()

st.sidebar.title("💬 Conversations")

if "threads" not in st.session_state:
  st.session_state.threads = {
      "Session Principale": "thread_oci_default"
  }  # Nom -> ID

if "current_thread_name" not in st.session_state:
  st.session_state.current_thread_name = "Session Principale"

# Bouton pour créer une nouvelle conversation
new_chat_name = st.sidebar.text_input("Nom de la nouvelle session", "")
if st.sidebar.button("➕ Créer une nouvelle session"):
  if new_chat_name:
    thread_id = f"thread_{len(st.session_state.threads) + 1}"
    st.session_state.threads[new_chat_name] = thread_id
    st.session_state.current_thread_name = new_chat_name
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Historique des sessions")

for t_name in st.session_state.threads.keys():
  if st.sidebar.button(
      t_name,
      key=f"btn_{t_name}",
      use_container_width=True,
      type=(
          "primary"
          if t_name == st.session_state.current_thread_name
          else "secondary"
      ),
  ):
    st.session_state.current_thread_name = t_name
    st.rerun()

current_thread_id = st.session_state.threads[
    st.session_state.current_thread_name
]


# Historique de chat
if "messages_history" not in st.session_state:
  st.session_state.messages_history = {}

if current_thread_id not in st.session_state.messages_history:
  st.session_state.messages_history[current_thread_id] = []

# Stockage temporaire des documents source récupérés pour la dernière requête
if "last_retrieved_docs" not in st.session_state:
  st.session_state.last_retrieved_docs = {}


# Afficher un appercu des documents
col_chat, col_docs = st.columns([2, 1])

with col_chat:
  st.subheader(
      f"Discussion en cours : `{st.session_state.current_thread_name}`"
  )

  # Affichage de l'historique des messages de la session active
  for message in st.session_state.messages_history[current_thread_id]:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # Saisie utilisateur
  if user_query := st.chat_input(
      "Posez votre question sur les avis clients..."
  ):
    # Afficher le message utilisateur
    st.session_state.messages_history[current_thread_id].append(
        {"role": "user", "content": user_query}
    )
    with st.chat_message("user"):
      st.markdown(user_query)

    # Récupération des documents pertinents (RAG Retriever) pour l'aperçu
    retrieved_docs = retriever.invoke(user_query)
    st.session_state.last_retrieved_docs[current_thread_id] = retrieved_docs

    # Exécution de l'agent LangGraph avec persistance de la mémoire (thread_id)
    config = {"configurable": {"thread_id": current_thread_id}}

    with st.chat_message("assistant"):
      message_placeholder = st.empty()
      full_response = ""

      # Appel de l'agent LangGraph en streaming
      input_messages = {"messages": [HumanMessage(content=user_query)]}
      for step in agent_executor.stream(
          input_messages, config, stream_mode="updates"
      ):
        if "agent" in step and "messages" in step["agent"]:
          latest_msg = step["agent"]["messages"][-1]
          if latest_msg.content:
            full_response = latest_msg.content
            message_placeholder.markdown(full_response)

      # Si pas de réponse directe via le stream d'updates, fallback sur 
      # ke
      if not full_response:
        with st.spinner("En train de réfléchir..."):
          res = agent_executor.invoke(input_messages, config)
        full_response = res["messages"][-1].content
        message_placeholder.markdown(full_response)

    # Sauvegarde de la réponse de l'assistant
    st.session_state.messages_history[current_thread_id].append(
        {"role": "assistant", "content": full_response}
    )
    st.rerun()

# Panneau latéral droit : Aperçu des documents correspondants
with col_docs:
  st.markdown("### 📄 Sources & Documents")
  st.markdown(
      "Extrait des avis clients injectés dans le contexte pour la dernière"
      " requête :"
  )

  docs_to_show = st.session_state.last_retrieved_docs.get(
      current_thread_id, []
  )

  if docs_to_show:
    for idx, doc in enumerate(docs_to_show):
      with st.expander(
          f"Avis source n°{idx+1}",
          expanded=(idx == 0),
      ):
        st.markdown(f"**Contenu :**\n> {doc.page_content}")
        if doc.metadata:
          st.json(doc.metadata)
  else:
    st.info("Aucun document consulté pour le moment.")