from flask import Flask, jsonify, request
from models import Person, Session
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello():
    return jsonify(message="Hey Nikhil, happy server is running")

@app.route('/add_person', methods=['POST'])
def add_person():
    session = Session()
    try:
        data = request.json
        title = data.get('title', None)
        desc = data.get('desc', None)

        if not title or not desc:
            return jsonify(error="Title or description is missing"), 400

        
        new_person = Person(id=str(uuid.uuid4()), title=title, description=desc)

        session.add(new_person)
        session.commit()

        return jsonify(message=f"Data added for {new_person.title}"), 201
    except Exception as e:
        session.rollback()
        return jsonify(error=str(e)), 500
    finally:
        session.close()

@app.route('/get_persons', methods=['GET'])
def get_persons():
    session = Session()
    try:
        
        data = session.query(Person).all()
        data_list = [{"id": i.id, "title": i.title, "desc": i.description} for i in data]
        return jsonify(data=data_list), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        session.close()

@app.route('/getone_person/<string:id>', methods=['GET'])
def get_one_person(id):
    session = Session()
    try:
        
        person = session.query(Person).get(id)
        if person:
            data = {
                "id": person.id,
                "title": person.title,
                "desc": person.description
            }
            return jsonify(data=data), 200
        else:
            return jsonify(error="Person not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        session.close()

@app.route('/update_person/<string:id>', methods=['PUT'])
def update_person(id):
    session = Session()
    try:
        data = request.json
        title = data.get('title', None)
        desc = data.get('desc', None)

        if not title or not desc:
            return jsonify(error="Title or description is missing"), 400

        
        person = session.query(Person).get(id)

        if person:
            person.title = title
            person.description = desc
            session.commit()
            return jsonify(message=f"Data updated for {person.title}"), 200
        else:
            return jsonify(error="Person not found"), 404
    except Exception as e:
        session.rollback()
        return jsonify(error=str(e)), 500
    finally:
        session.close()

@app.route('/delete_person/<string:id>', methods=['DELETE'])
def delete_person(id):
    try:
        session = Session()
        person = session.query(Person).get(id)

        if person:
            session.delete(person)
            session.commit()
            return jsonify(message=f"Data deleted for {person.title}"), 200
        else:
            return jsonify(error="Person not found"), 404
    except Exception as e:
        session.rollback()
        return jsonify(error=str(e)), 500
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
