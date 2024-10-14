from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

app = Flask(__name__)

# Datenbank-Verbindung konfigurieren
DATABASE_URL = "postgresql+pg8000://roman:PASSWORD@HOST:5432/accessdata"
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
    email = Column(String, nullable=False)

# Route zum Erstellen der Tabelle
@app.route('/create_users_table')
def create_users_table():
    try:
        Base.metadata.create_all(engine)
        return {"message": "Tabelle 'users' erfolgreich erstellt!"}
    except Exception as e:
        return {"error": str(e)}

# Route zum Hinzufügen eines Benutzers
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    try:
        new_user = User(name=data['name'], email=data['email'])
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
        users = session.query(User).all()
        return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users])
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.remove()  # Session am Ende entfernen

# Debugging-Route, um Tabellen zu überprüfen
@app.route('/debug_db')
def debug_db():
    try:
        conn = engine.connect()
        tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';").fetchall()
        return {"tables": [table[0] for table in tables]}
    except Exception as e:
        return {"error": str(e)}

# Startpunkt der App
if __name__ == '__main__':
    app.run(debug=True)
