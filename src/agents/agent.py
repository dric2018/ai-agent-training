import abc
import datetime
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.config import CFG

import os

load_dotenv()


class Agent(abc.ABC):
    def __init__(
            self, 
            vllm_url:str=CFG.VLLM_BASE_URL,
        ):
        self.model_name = CFG.BASE_MODEL

        date = datetime.now().strftime("%Y—%m-%d")
        year = date.split("-")[0]

        self.system_prompt = ChatPromptTemplate.from_messages([
            ("system", f"""Today is {date}. We are in the year {year}.\n
                You are an expert AI engineer working in the telecom sector. 
                You will be asked to complete tasks based  
            """),
            ("human", "Hello, how are you doing?"),
            ("ai", "I'm doing well, thanks! How can I help you ?"),
            ("human", "{user_input}"),
        ])

        # chain
        self.llm = ChatOpenAI(
            openai_api_base=vllm_url, 
            # base_url=f"http://localhost:{CFG.VLLM_PORT}/v1",
            api_key=CFG.OPEN_API_KEY,
            max_completion_tokens=CFG.MAX_TOKENS,
            temperature=CFG.GENERATION_TEMPERATURE,
            model=CFG.BASE_MODEL,
            extra_body={
                "reasoning_effort": CFG.REASONING_EFFORT,
                "chat_template_kwargs": {"enable_thinking": False},
            },
            streaming=CFG.IS_STREAM,
            timeout=CFG.TIMEOUT,
            max_retries=3
        )
        self.chain     = self.init_prompt | self.llm

    @staticmethod
    def get_answer(user_prompt:str):
        pass


                