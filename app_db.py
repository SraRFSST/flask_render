from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import bcrypt
from sqlalchemy import text

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
    pwh = Column(String, nullable=False)  # Speichert den Passwort-Hash

# Route zum Erstellen der Tabelle
@app.route('/create_users_table')
def create_users_table():
    try:
        Base.metadata.create_all(engine)  # Erstellen der Tabelle
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

# Route zum Hinzufügen einer Spalte 'pwh'
@app.route('/add_pwh_column')
def add_pwh_column():
    try:
        session.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS pwh VARCHAR;")
        session.commit()
        return {"message": "Spalte 'pwh' erfolgreich hinzugefügt!"}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.remove()  # Session am Ende entfernen

# Route zum Löschen der Spalte 'email'
@app.route('/drop_email_column')
def drop_email_column():
    try:
        conn = engine.connect()
        # Text muss explizit als text() deklariert werden
        conn.execute(text("ALTER TABLE users DROP COLUMN IF EXISTS email;"))
        conn.close()
        return {"message": "Spalte 'email' erfolgreich entfernt!"}
    except Exception as e:
        return {"error": str(e)}

# Debugging-Route, um Tabellen zu überprüfen
@app.route('/debug_columns')
def debug_columns():
    try:
        columns = session.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'users';").fetchall()
        return {"columns": [column[0] for column in columns]}
    except Exception as e:
        return {"error": str(e)}

# Startpunkt der App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
