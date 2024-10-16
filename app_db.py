from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, JWTManager
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import bcrypt

app = Flask(__name__)

# CORS für alle Routen und Domains aktivieren
CORS(app)

# Ein Geheimschlüssel wird für die JWT-Generierung benötigt
app.config['JWT_SECRET_KEY'] = 'dein-geheimer-schluessel'  # Ersetze durch einen sicheren Schlüssel

# Initialisierung der JWT-Erweiterung
jwt = JWTManager(app)

# Datenbank-Verbindung konfigurieren
DATABASE_URL = "postgresql+pg8000://roman:8wyGMUqyvv3YR8WZ155c04H1PfuP1iHY@dpg-cs7ac4lds78s73b9foj0-a:5432/accessdata_jx7t"
engine = create_engine(DATABASE_URL)

# Session konfigurieren
SessionFactory = sessionmaker(bind=engine)
session = scoped_session(SessionFactory)

# Basis für das ORM-Modell
Base = declarative_base()

# User-Modell definieren
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    pwh = Column(String, nullable=False)  # Speichert den Passwort-Hash

# Route zum Erstellen der Tabelle
@app.route('/create_users_table')
def create_users_table():
    try:
        Base.metadata.create_all(engine)  # Erstellen der Tabelle
        return {"message": "Tabelle 'users' erfolgreich erstellt!"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        usr = data['name']
        # Passwort hashen
        password = data['password'].encode('utf-8')
        pwh = bcrypt.hashpw(password, bcrypt.gensalt())

        user = session.query(User).filter_by(name=usr).first()

        if user:
            if bcrypt.checkpw(password, user.pwh.encode('utf-8')):
                access_token = create_access_token(identity=usr)
                return jsonify({"token":access_token, "message": f"User {usr} erfolgreich eingeloggt"}), 201
            else:
                return jsonify({"message": "Falsches Passwort"}), 401
        else:
            return jsonify({"message": f"User {usr} nicht bekannt"}), 400
    except Exception as e:
        session.close()
        return jsonify({"error": str(e)}), 400
    finally:
        session.remove()  # Sicherstellen, dass Session geschlossen wird


# Route zum Hinzufügen eines Benutzers mit Passwort-Hashing
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    try:
        # Passwort hashen
        password = data['password'].encode('utf-8')
        pwh = bcrypt.hashpw(password, bcrypt.gensalt())

        new_user = User(name=data['name'], pwh=pwh.decode('utf-8'))
        session.add(new_user)
        session.commit()
        return jsonify({"message": "User added successfully!"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.remove()  # Session am Ende entfernen

# Route zum Auflisten aller Benutzer
@app.route('/list_users', methods=['GET'])
def list_users():
    try:
        users = session.query(User).all()  # Alle Benutzer abfragen
        return jsonify([{"id": user.id, "name": user.name, "password_hash": user.pwh} for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.remove()  # Session am Ende entfernen



# Startpunkt der App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
