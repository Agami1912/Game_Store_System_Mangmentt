from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
game_bp = Blueprint('game', __name__, url_prefix='/games')
customer_bp = Blueprint('customer', __name__, url_prefix='/customers')
loan_bp = Blueprint('loan', __name__, url_prefix='/loans')
