from flask import Flask, request, jsonify # type: ignore
from src.api.controllers.user_controller import UserController

app = Flask(__name__)
user_controller = UserController()

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = user_controller.create_user(data)
    return jsonify(user), 201

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = user_controller.get_user(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    user = user_controller.update_user(user_id, data)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    success = user_controller.delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404
