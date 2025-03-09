from flask import Blueprint, request, jsonify
from models import db, Customer, Loan

customer_bp = Blueprint("customer", __name__, url_prefix="/customers")


@customer_bp.route("/", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{"id": c.id, "name": c.name, "email": c.email, "phone": c.phone} for c in customers])


@customer_bp.route("/", methods=["POST"])
def add_customer():
    data = request.json
    new_customer = Customer(name=data["name"], email=data["email"], phone=data["phone"])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Customer added successfully"}), 201


@customer_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)


    Loan.query.filter_by(customer_id=customer_id).delete()

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer and related loans deleted successfully"})
