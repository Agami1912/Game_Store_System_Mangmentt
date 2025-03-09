from flask import Blueprint, request, redirect, url_for, render_template, session
from models.admin import Admin

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            session["admin_id"] = admin.id
            return redirect(url_for("home"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("admin_id", None)
    return redirect(url_for("auth.login"))
