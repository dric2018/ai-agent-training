# ai-agent-training

## commandes 
python3 -m venv ai-agents # créer un environnement virtuel

pip install -r requirements.txt


## Installer uv 

https://docs.astral.sh/uv/#highlights

sur mac/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh

## Activer l'environnement virtuel
### Linux
source .venv/bin/activate 

### Command Prompt (CMD)
.\venv\Scripts\activate.bat

### PowerShell
.\venv\Scripts\Activate.ps1

### Git Bash / WSL

source venv/Scripts/activate


### Installer n8n en local

NB: Vous aurez besoin d'avoir `nodeJS` déjà installer
````bash 
npm install n8n -g
````

````bash 
n8n start
````

Vous pouvez accéder à l'interface via: `http://localhost:5678`

## Prompt pour n8n
```
[ROLE]
Tu es un expert en analyse de la relation client pour les télécoms. 
[TACHE]
Classe l'avis client suivant en trois catégories : 
- Sentiment (Positif/Négatif/Neutre)
- Thématique (Facturation/Technique/Réseau)
- Urgence (Faible/Moyenne/Haute).
[FORMAT]
Réponds sous forme de bullet points.
```