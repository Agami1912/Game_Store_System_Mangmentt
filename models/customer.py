from . import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    games = db.relationship('Game', backref='customer', lazy=True)

    def __repr__(self):
        return f"<Customer {self.name} - {self.email}>"
