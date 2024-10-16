# Render-Demo-Server
Es wird eine Flask-Backend-Anwendung entwickelt, die auf http://render.com gehostet wird

Grundsätzliche Struktur:  
- lauffähiges Python Skript `app.py` in einem Wurzelverzeichnis  
- `requirements.txt` mit den notwendigen Paketen ebenfalls im gleichen Verzeichnis  
- Erstellen von `requirements.txt`:  
    - Erstellen einer virtuellen Umgebung `pip -m venv .venv`  
    - Starten `.venv\bin\Activate.ps1`  
    - Installieren von Paketen `pip install Flask gunicorn` ...  
    - Datei erzeugen `pip freeze > requirements.txt`  
- der Ordner wir in einem Verzeichnis als git-Repository verwaltet (hier GitHub-Projekt `flask_render`)  
- Unter `render.com` wurde ein Projekt `backend` erzeugt und ein WebService `flask_render` erstellt.  
- für den `flask-render`-WebService wurde in den Einstellungen gesetzt:  
    - Name: `flask_render`
    - GitHub-Repo: `https://github.com/SraRFSST/flask_render`
    - Build Command: `pip install -r requirements.txt`
    - Start Command: `gunicorn app:app`  (erstes `app`: Name des Skripts, zweites `app`: Name der Funktion)  
    - erzeugt wird: 
- Erzeugen `Manual Deploy`: dabei wird die Umgebung erzeugt und das Skript gestartet  

## Zugriff
https://flask-render-yjoh.onrender.com  
(Routes: `/` und `hallo`) also  
https://flask-render-yjoh.onrender.com/  
https://flask-render-yjoh.onrender.com/hallo  

## Deployen
Wenn Änderungen gemacht werden, diese auf GitHub pushen und manuell auf render Deployen.


# Anwendung mit DB
Eine zweite Anwendung `app_db.py` greift auf eine Datenbank zu, die ebenfalls auf `Render` gehostet wird.

## Installation Postgres
für eine lokale Postgres-Installation (nicht notwendig):  
- Download von https://www.enterprisedb.com/downloads/postgres-postgresql-downloads  
- Installation mit Standard-Einstellungen  
  user (Admin) postgres  / roman
  pass (Admin) comein    / iNC3sEhZkLR16BcyYjYG8WBPX25hv4Hc
  port 5432  
  Dienst wird automatisch gestartet  
  Test: `"c:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres`

auf `Render` kann eine PostgreSQL erzeugt werden. Die Einstellungen:  
- Name: `backend_db`  
- Port: `5432`  
- Database: `accessdata_jx7t` (wurde angepasst, weil schon vorh.)  
- Username: `roman` 
- Password: `8wyGMUqyvv3YR8WZ155c04H1PfuP1iHY` (wird erzeugt)
- Host: `8wyGMUqyvv3YR8WZ155c04H1PfuP1iHY` (wird erzeugt)

in Python wird installiert:   
`pip install Flask sqlalchemy pg8000`  
damit ein neues `requirements_db.txt` erzeugt  

## Zugriff:
- Erstellen der `users`-Tabelle (einmalig notwendig):  
https://flask-db-71xi.onrender.com/create_users_table  
- Zeigen der eingetragenen Namen:  
https://flask-db-71xi.onrender.com/list_users
- Eintragen eines Datensatzes (z.B. mit Curl):  
`curl -X POST -H "Content-Type: application/json" -d "{\"name\":\"Jane Doe\",\"password\":\"su
persecurepassword\"}" https://flask-db-71xi.onrender.com/add_user`

beim Anzeigen der User wird ersichtlich - die Passwörter wurden als Hash abgelegt. Weiters: wenn verschiedene User die gleichen Passwörter anlegen, dann haben sie einen verschiedenen Hash-Wert.
