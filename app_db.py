from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# SQLAlchemy Setup
DATABASE_URI = 'postgresql+pg8000://roman:iNC3sEhZkLR16BcyYjYG8WBPX25hv4Hc@dpg-cs6knaij1k6c73a5uqi0-a:5432/accessdata'
engine = create_engine(DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

# Route zum Hinzufügen eines Benutzers
@app.route('/add_user', methods=['POST'])
def add_user():
    session = Session()
    try:
        data = request.json
        new_user = User(name=data['name'], email=data['email'])
        session.add(new_user)
        session.commit()
        return jsonify({'message': 'Benutzer erfolgreich hinzugefügt!'}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

# Route zum Abrufen aller Benutzer
@app.route('/users', methods=['GET'])
def get_users():
    session = Session()
    try:
        users = session.query(User).all()
        return jsonify([{ 'id': user.id, 'name': user.name, 'email': user.email } for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route('/debug_db')
def debug_db():
    try:
        # Überprüfen, ob die Verbindung zur Datenbank funktioniert
        conn = engine.connect()
        # Tabellen auflisten
        tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';").fetchall()
        return {"tables": [table[0] for table in tables]}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Stelle sicher, dass die Tabelle existiert
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', port=5000)

