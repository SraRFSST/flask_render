# Render-Demo-Server
Dieses Projekt wird auf http://render.com gehostet.

Dazu wird das GitHub-Repo dort bei Änderungen deployed und ist verfügbar unter:
https://render-kram.onrender.com/hallo  

## Setup
Name: `flask_backend`  
Git-Repo: `https://github.com/SraRFSST/flask_render`  
Build Command: `pip install -r requirements.txt`  
Start Command : `gunicorn app:app`  
Für Render wird `gunicorn` benötigt  
## Zugriff
https://flask-render-yjoh.onrender.com/hallo  
(`hallo` ist die Route)

## Deployen
Wenn Änderungen gemacht werden, diese auf GitHub pushen und manuell auf render Deployen.