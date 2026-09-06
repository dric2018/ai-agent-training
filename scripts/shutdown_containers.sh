#/bin/bash
docker stop vllm nginx streamlit-app prometheus grafana
docker compose down
docker ps