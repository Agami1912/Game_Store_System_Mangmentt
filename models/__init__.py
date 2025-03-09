from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

from .game import Game
from .customer import Customer
from .admin import Admin
from .loan import Loan
