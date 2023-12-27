from . import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSONB

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    loginuser = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(102), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    userage = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    gender_poisk = db.Column(db.String(10), nullable=False)
    info = db.Column(db.Text)
    is_public = db.Column(db.Boolean)
