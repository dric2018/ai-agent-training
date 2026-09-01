from datetime import datetime
import zoneinfo  

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, HumanMessage

from langchain.agents import create_agent
from config import CFG

import os

from tools import search_past_reviews
import streamlit as st

from __init__ import logger

load_dotenv()


@st.cache_resource
def init_agent():
  model = ChatOpenAI(
    model="gpt-4o-mini",#CFG.BASE_MODEL, 
    temperature=CFG.GENERATION_TEMPERATURE
  )

  logger.info(f"Initialisation de l'agent avec le modèle {model.model_name}...")
  
  memory = MemorySaver()

  tz_abidjan = zoneinfo.ZoneInfo("Africa/Abidjan")
  maintenant = datetime.now(tz_abidjan)
  today = maintenant.strftime("%d/%m/%Y à %H:%M")

  logger.info("Création de l'agent...")
  with open(os.path.join(CFG.PROJECT_ROOT, "prompts/system_prompt_OCI_Voice.txt"), "r") as f:
    prompt = f.read()

  prompt = prompt.format(today=today)  
  system_prompt = SystemMessage(
      content=prompt
    )

  # Création de l'agent ReAct de LangGraph
  agent = create_agent(
      model=model, 
      tools=[search_past_reviews], 
      checkpointer=memory, 
      system_prompt=system_prompt
  )

  logger.info("Agent créé avec sucès!")
  
  return agent

def test_agent_trace(streaming:bool=False):
    # Vérification de l'activation de LangSmith
    if os.getenv("LANGSMITH_TRACING") != "true":
        print("Avertissement : LANGSMITH_TRACING n'est pas activé à 'true' dans votre .env")

    agent = init_agent()
    # Configuration avec un thread_id pour tester la persistance
    config = {"configurable": {"thread_id": "test_trace_thread_01"}}

    # Requête de test simulant un utilisateur
    user_query = "Quels sont les principaux problèmes de connexion internet rencontrés par les clients ?"
    print(f"\nQ: {user_query}")

    input_data = {"messages": [HumanMessage(content=user_query)]}
    if streaming:
      for step in agent.stream(input_data, config, stream_mode="updates"):
        for node_name, node_output in step.items():
          print("-"*25)
          print(f"[Noeud actif : {node_name}]")
          print("-"*25)
          if "messages" in node_output:
              for msg in node_output["messages"]:
                  
                  # Affichage des messages générés ou des appels d'outils
                  print(f"Type de Msg ({type(msg).__name__})")
                  print(f"Contenu: >>{msg.content}<<\n")
    else:     
      logger.info("Exécution de l'agent et génération de la trace LangSmith...")
      # import pdb; pdb.set_trace()
      response = agent.invoke(input_data, config)

      print("\n--- Réponse finale de l'Agent ---")
      last_message = response["messages"][-1]
      print(last_message.content)

    logger.info("\nExécution terminée. Rendez-vous sur votre dashboard LangSmith (https://smith.langchain.com) pour inspecter la trace du graphe.")

if __name__ == "__main__":
  # agent = init_agent()

  test_agent_trace(streaming=True)
  
                