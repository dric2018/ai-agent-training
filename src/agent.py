from datetime import datetime
import zoneinfo  

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage

from langchain.agents import create_agent
from config import CFG

from pprint import pprint
import os

import streamlit as st

load_dotenv()


@st.cache_resource
def init_agent():
  model = ChatOllama(
    model=CFG.BASE_MODEL, 
    temperature=CFG.GENERATION_TEMPERATURE
  )
  
  memory = MemorySaver()

  tz_abidjan = zoneinfo.ZoneInfo("Africa/Abidjan")
  maintenant = datetime.now(tz_abidjan)
  today = maintenant.strftime("%d/%m/%Y à %H:%M")

  with open(os.path.join(CFG.PROJECT_ROOT, "prompts/system_prompt_OCI_Voice.txt"), "r") as f:
    prompt = f.read()

  prompt = prompt.format(today=today)
  pprint(prompt)
  
  system_prompt = SystemMessage(
      content=prompt
    )

  # Création de l'agent ReAct de LangGraph
  agent = create_agent(
      model=model, 
      tools=[], 
      checkpointer=memory, 
      system_prompt=system_prompt
  )
  return agent


if __name__ == "__main__":
  agent = init_agent()
                