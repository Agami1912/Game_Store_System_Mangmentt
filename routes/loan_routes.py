from flask import Blueprint, request, jsonify
from models import db, Loan, Game, Customer

loan_bp = Blueprint("loan", __name__, url_prefix="/loans")

@loan_bp.route("/", methods=["GET"])
def get_loaned_games():
    loans = Loan.query.all()
    return jsonify([{"id": l.id, "title": l.game.title, "customer": l.customer.name} for l in loans])

@loan_bp.route("/", methods=["POST"])
def loan_game():
    data = request.json
    game = Game.query.get_or_404(data["game_id"])
    customer = Customer.query.get_or_404(data["customer_id"])

    if game.quantity <= 0:
        return jsonify({"message": "Game is out of stock"}), 400

    new_loan = Loan(game_id=game.id, customer_id=customer.id)
    game.quantity -= 1
    db.session.add(new_loan)
    db.session.commit()
    return jsonify({"message": "Game loaned successfully", "quantity": game.quantity}), 201

@loan_bp.route("/loans/<int:loan_id>", methods=["DELETE"])
def return_game(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    game = loan.game

    game.quantity += 1
    db.session.delete(loan)
    db.session.commit()

    return jsonify({"message": "Game returned successfully", "quantity": game.quantity})
