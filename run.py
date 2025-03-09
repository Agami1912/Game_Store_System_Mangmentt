from flask import Flask, render_template, redirect, url_for, session
from models import db
from routes.auth import auth_bp
from routes.game_routes import game_bp
from routes.customer_routes import customer_bp
from routes.loan_routes import loan_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(game_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(loan_bp)

@app.route("/")
def home():
    if "admin_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
