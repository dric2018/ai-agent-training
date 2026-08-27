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
    NGINX_PORT              = os.getenv("NGINX_PORT", "8080")
    LLM_BACKEND_PORT        = os.getenv("VLLM_PORT", "8000")

    SERVER_IP               = str(os.getenv("SERVER_IP", "127.0.0.1"))
    USERNAME                = os.getenv("USERNAME", "")
    DOCKER_CON_IP           = "http://host.docker.internal"
    API_KEY                 = os.getenv("OPENAI_API_KEY", "token-is-ignored")
    HF_TOKEN                = os.getenv('HF_TOKEN', '')
    # BASE_URL                = f"http://{SERVER_IP}:{LLM_BACKEND_PORT}/v1"
    BASE_URL                = str(os.getenv("RUNPOD_API_URL", ""))

    # DB Paths
    DB_DIR                  = osp.join(PROJECT_ROOT, "storage/duckdb")
    DB_NAME                 = "clients.duckdb"
    DB_PATH                 = osp.join(DB_DIR, DB_NAME)
    
    # SQL Guardrails
    ALLOWED_TABLES          = [
                               ]
    # DB
    SQL_MAX_LIMIT           = 20
    TOP_K                   = 10
    
    # LLM (vLLM) Settings
    IS_STREAM               = False
    BASE_MODEL              = os.getenv("BASE_MODEL", "Qwen/Qwen3-4B-Instruct-2507")
    EMBEDDING_MODEL_NAME    = "google/embeddinggemma-300m" #"sentence-transformers/all-MiniLM-L6-v2" (384d)
    TARGET_EMBEDDING_DIM    = 512
    MODEL_PROVIDER          = "openai"
    RELEVANCE_THRESHOLD     = 0.8 
    GENERATION_TEMPERATURE  = 0.3 # 1 for reasoning models
    MAX_MODEL_LEN           = os.getenv("MAX_MODEL_LEN", 32000)
    MAX_TOKENS              = 4096
    CHUNK_SIZE              = 256
    CHUNK_OVERLAP           = 100
    REASONING_EFFORT        = "low" # Options: "low", "medium", "high"
    MAX_ITERATIONS          = 18
    TIMEOUT                 = 300


    
os.chdir(CFG.PROJECT_ROOT)

if __name__=="__main__":
    pprint(vars(CFG))
