from flask import Blueprint, request, jsonify
from models import db, Game

game_bp = Blueprint("game", __name__)

# ✅ GET all games
@game_bp.route("/games", methods=["GET"])
def get_games():
    games = Game.query.all()
    return jsonify([
        {"id": g.id, "title": g.title, "genre": g.genre, "price": g.price, "quantity": g.quantity}
        for g in games
    ])


@game_bp.route("/games", methods=["POST"])
def add_game():
    data = request.json
    new_game = Game(title=data["title"], genre=data["genre"], price=data["price"], quantity=data["quantity"])
    db.session.add(new_game)
    db.session.commit()
    return jsonify({"message": "Game added successfully"}), 201

@game_bp.route("/games/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return jsonify({"message": "Game deleted successfully"})
