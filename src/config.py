from dotenv import load_dotenv
load_dotenv() # Loading vars from .env

import os
import os.path as osp

from pathlib import Path
from pprint import pprint

def get_project_root() -> Path:
    """Finds the root by looking for a marker file."""
    current_path = Path(__file__).resolve()

    for parent in current_path.parents:
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
            return parent

    return current_path.parent

class CFG:
    PROJECT_ROOT            = get_project_root()
    LOGS_DIR                = osp.join(PROJECT_ROOT, "logs")
    DATA_DIR                = osp.join(PROJECT_ROOT, "data/french-customer-review-sentiment-free-2k")

    DEBUG_MODE              = True

    # Server settings
    UI_PORT                 = os.getenv("UI_PORT", 8501)
    LLM_BACKEND_PORT        = os.getenv("LLM_API_PORT", "8000")

    SERVER_IP               = str(os.getenv("SERVER_IP", "127.0.0.1"))
    USERNAME                = os.getenv("USERNAME", "")
    DOCKER_CON_IP           = "http://host.docker.internal"
    API_KEY                 = os.getenv("OPENAI_API_KEY", "token-is-ignored")
    HF_TOKEN                = os.getenv('HF_TOKEN', '')
    # BASE_URL                = f"http://{SERVER_IP}:{LLM_BACKEND_PORT}/v1"
    
    TOP_K                   = 10
    
    # LLM (vLLM) Settings
    BASE_MODEL              = "mistral:7b"
    EMBEDDING_MODEL_NAME    = "google/embeddinggemma-300m" #"sentence-transformers/all-MiniLM-L6-v2" (384d)
    TARGET_EMBEDDING_DIM    = 512
    MODEL_PROVIDER          = "openai"
    GENERATION_TEMPERATURE  = 0.3 # 1 for reasoning models
    REASONING_EFFORT        = "low" # Options: "low", "medium", "high"
    MAX_ITERATIONS          = 10
    TIMEOUT                 = 300


    
os.chdir(CFG.PROJECT_ROOT)

if __name__=="__main__":
    pprint(vars(CFG))
