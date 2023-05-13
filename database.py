from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dnd.db'
db = SQLAlchemy(app)

class UserType(db.Model):
    id_user_type = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_type = db.Column(db.String(50), nullable=False)


class Class(db.Model):
    id_class = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(50), nullable=False)


class RacialGroup(db.Model):
    id_racial_group = db.Column(db.Integer, primary_key=True, autoincrement=True)
    racial_group = db.Column(db.String(50), nullable=False)


class Equipment(db.Model):
    id_equipment = db.Column(db.Integer, primary_key=True, autoincrement=True)
    equipment = db.Column(db.String(50), nullable=False)


class Proficiency(db.Model):
    id_profishiency = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proficiency = db.Column(db.String(50), nullable=False)


class Note(db.Model):
    id_note = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(2000), nullable=False)


class Attack(db.Model):
    id_attack = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    attack_bonus = db.Column(db.Integer, nullable=False)
    damage_type = db.Column(db.String(100), nullable=False)


class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    id_user_type = db.Column(db.Integer, db.ForeignKey('user_type.id_user_type'), nullable=False)
    user_type = db.relationship('UserType', backref=db.backref('users', lazy=True))


class Character(db.Model):
    id_character = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    constitution = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    wisdom = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
    armor_class = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    initiative = db.Column(db.Integer, nullable=False)
    health_current = db.Column(db.Integer, nullable=False)
    health_max = db.Column(db.Integer, nullable=False)
    profishiency_bonus = db.Column(db.Integer, nullable=False)
    inspiration = db.Column(db.Integer, nullable=False)

id_attack = db.Column(db.Integer, db.ForeignKey('attack.id_attack'), nullable=False)
id_note = db.Column(db.Integer, db.ForeignKey('note.id_note'), nullable=False)
id_class = db.Column(db.Integer, db.ForeignKey('class.id_class'), nullable=False)
id_racial_group = db.Column(db.Integer, db.ForeignKey('racial_group.id_racial_group'), nullable=False)
id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
attack = db.relationship('Attack', backref=db.backref('characters', lazy=True))
note = db.relationship('Note', backref=db.backref('characters', lazy=True))
class_ = db.relationship('Class', backref=db.backref('characters', lazy=True))
racial_group = db.relationship('RacialGroup', backref=db.backref('characters', lazy=True))
user = db.relationship('User', backref=db.backref('characters', lazy=True))

