#!/bin/bash

# Par défaut, démarre les conteneurs existants sans reconstruire
BUILD_FLAG=""

# Vérifie si l'utilisateur a passé explicitement --build ou --recreate en argument
for arg in "$@"; do
    if [ "$arg" = "--build" ] || [ "$arg" = "--recreate" ]; then
        BUILD_FLAG="--build --force-recreate"
        echo "Option de reconstruction détectée. Reconstruction des conteneurs..."
        break
    fi
done

if [ -z "$BUILD_FLAG" ]; then
    echo "Démarrage des conteneurs existants (sans reconstruction)..."
fi

# Exécution de docker compose avec ou sans le flag de build
docker compose up -d $BUILD_FLAG vllm streamlit-app nginx