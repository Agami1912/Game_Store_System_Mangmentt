from . import db

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    game = db.relationship('Game', backref='loans')
    customer = db.relationship('Customer', backref='loans')

    def __repr__(self):
        return f"<Loan {self.game.title} to {self.customer.name}>"
