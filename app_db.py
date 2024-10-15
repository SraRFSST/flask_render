from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import bcrypt

app = Flask(__name__)

# Datenbank-Verbindung konfigurieren
DATABASE_URL = "postgresql+pg8000://roman:iNC3sEhZkLR16BcyYjYG8WBPX25hv4Hc@dpg-cs6knaij1k6c73a5uqi0-a:5432/accessdata"
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
    password_hash = Column(String, nullable=False)  # Speichert den Passwort-Hash

# Route zum Erstellen der Tabelle
@app.route('/create_users_table')
def create_users_table():
    try:
        Base.metadata.create_all(engine)
        return {"message": "Tabelle 'users' erfolgreich erstellt!"}
    except Exception as e:
        return {"error": str(e)}

# Route zum Hinzufügen eines Benutzers mit Passwort-Hashing
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    try:
        # Passwort hashen
        password = data['password'].encode('utf-8')
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())

        new_user = User(name=data['name'], password_hash=password_hash.decode('utf-8'))
        session.add(new_user)
        session.commit()
        return jsonify({"message": "User added successfully!"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.remove()  # Session am Ende entfernen

# Route zum Überprüfen eines Benutzernamens und Passworts
@app.route('/verify_user', methods=['POST'])
def verify_user():
    data = request.get_json()
    try:
        user = session.query(User).filter_by(name=data['name']).first()
        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password_hash.encode('utf-8')):
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.remove()  # Session am Ende entfernen

# Route zum Auflisten aller Benutzer (nur für Debugging)
@app.route('/list_users', methods=['GET'])
def list_users():
    try:
        users = session.query(User).all()
        return jsonify([{"id": user.id, "name": user.name} for user in users])
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.remove()  # Session am Ende entfernen

# Debugging-Route, um Tabellen zu überprüfen
@app.route('/debug_db')
def debug_db():
    try:
        conn = engine.connect()
        # Abfrage, um alle Tabellen im Schema 'public' zu erhalten
        tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';").fetchall()
        return {"tables": [table[0] for table in tables]}
    except Exception as e:
        return {"error": str(e)}

@app.route('/debug_columns')
def debug_columns():
    try:
        conn = engine.connect()
        # Abfrage, um alle Spalten der Tabelle 'users' zu erhalten
        columns = conn.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'users';").fetchall()
        return {"columns": [column[0] for column in columns]}
    except Exception as e:
        return {"error": str(e)}


# Startpunkt der App
if __name__ == '__main__':
    app.run(debug=True)
