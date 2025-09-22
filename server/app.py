from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # GET /messages → all messages ordered by created_at ASC
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([m.to_dict() for m in messages]), 200

    elif request.method == 'POST':
        # POST /messages → create new message
        data = request.get_json()
        new_msg = Message(
            body=data.get("body"),
            username=data.get("username"),
        )
        db.session.add(new_msg)
        db.session.commit()
        return jsonify(new_msg.to_dict()), 201


@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    msg = Message.query.get(id)

    if not msg:
        return jsonify({"error": "Message not found"}), 404

    if request.method == 'GET':
        return jsonify(msg.to_dict()), 200

    elif request.method == 'PATCH':
        data = request.get_json()
        if "body" in data:
            msg.body = data["body"]
        db.session.commit()
        return jsonify(msg.to_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(msg)
        db.session.commit()
        return jsonify({"delete_successful": True, "message": f"Message {id} deleted"}), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
