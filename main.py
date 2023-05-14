from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, Blueprint, render_template, url_for, send_file, request, flash, redirect, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, current_user, UserMixin, LoginManager, logout_user
import json
app = Flask(__name__, static_folder='static')
db = SQLAlchemy()
app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dnd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))


def all_monsters():
    f = open("./static/json/monsters.json")
    data = json.load(f)
    monsters = {}
    for i in data.get('results'):
        monsters[i['name']] = [i['url'][13:], i['index']]
    f.close()
    return monsters


monsters1 = all_monsters()


@app.route("/bestiary/<monsters_name>")
def detail_bestiary(monsters_name):
    for_api_key = ''
    monster_properties = {}
    for key, value in monsters1.items():
        if (monsters_name.lower() == value[1].lower()):
            for_api_key = value[1]
            f = open(
                f"./static/json/all_types_details/monsters/{for_api_key}.json")
            data = json.load(f)
            monster_properties = {}
            try:
                monster_properties["name"] = data["name"]
            except (IndexError, KeyError):
                monster_properties["name"] = "-"
            try:
                monster_properties["type"] = data["type"]
            except (IndexError, KeyError):
                monster_properties["type"] = "-"
            try:
                monster_properties["armor_class"] = data["armor_class"][0]["value"]
            except (IndexError, KeyError):
                monster_properties["armor_class"] = "-"
            try:
                monster_properties["speed_walk"] = data["speed"]["walk"]
            except (IndexError, KeyError):
                monster_properties["speed_walk"] = "-"
            try:
                monster_properties["speed_swim"] = data["speed"]["swim"]
            except (IndexError, KeyError):
                monster_properties["speed_swim"] = "-"
            try:
                monster_properties["strength"] = data["strength"]
            except (IndexError, KeyError):
                monster_properties["strength"] = "-"
            try:
                monster_properties["dexterity"] = data["dexterity"]
            except (IndexError, KeyError):
                monster_properties["dexterity"] = "-"
            try:
                monster_properties["constitution"] = data["constitution"]
            except (IndexError, KeyError):
                monster_properties["constitution"] = "-"
            try:
                monster_properties["intelligence"] = data["intelligence"]
            except (IndexError, KeyError):
                monster_properties["intelligence"] = "-"
            try:
                monster_properties["wisdom"] = data["wisdom"]
            except (IndexError, KeyError):
                monster_properties["wisdom"] = "-"
            try:
                monster_properties["charisma"] = data["charisma"]
            except (IndexError, KeyError):
                monster_properties["charisma"] = "-"
            try:
                monster_properties["damage_vulnerabilities"] = data["damage_vulnerabilities"]
            except (IndexError, KeyError):
                monster_properties["damage_vulnerabilities"] = []
            try:
                monster_properties["damage_resistances"] = data["damage_resistances"]
            except (IndexError, KeyError):
                monster_properties["damage_resistances"] = []
            try:
                monster_properties["damage_immunities"] = data["damage_immunities"]
            except (IndexError, KeyError):
                monster_properties["damage_immunities"] = []
            try:
                monster_properties["challenge_rating"] = data["challenge_rating"]
            except (IndexError, KeyError):
                monster_properties["challenge_rating"] = "-"
            try:
                monster_properties["hit_points"] = data["hit_points"]
            except (IndexError, KeyError):
                monster_properties["hit_points"] = "-"
            try:
                monster_properties["special_abilities_name"] = data["special_abilities"][0]["name"]
            except (IndexError, KeyError):
                monster_properties["special_abilities_name"] = "-"
            try:
                monster_properties["special_abilities_desc"] = data["special_abilities"][0]["desc"]
            except (IndexError, KeyError):
                monster_properties["special_abilities_desc"] = "-"
            try:
                monster_properties["action_name"] = data["actions"][0]["name"]
            except (IndexError, KeyError):
                monster_properties["action_name"] = "-"
            try:
                monster_properties["action_desc"] = data["actions"][0]["desc"]
            except (IndexError, KeyError):
                monster_properties["action_desc"] = "-"
            try:
                monster_properties["attack_bonus"] = data["actions"][0]["attack_bonus"]
            except (IndexError, KeyError):
                monster_properties["attack_bonus"] = "-"
            try:
                monster_properties["damage_type"] = data["actions"][0]["damage"][0]["damage_type"]["index"]
            except (IndexError, KeyError):
                monster_properties["damage_type"] = "-"
            try:
                monster_properties["image"] = data["image"]
            except (IndexError, KeyError):
                monster_properties["image"] = ""
    return render_template("bestiary.html", dict_monster_prop=monster_properties, monsters=monsters1)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/merche.html")
def merche():
    return render_template("merche.html")


@app.route('/charlist.html')
@login_required
def charlist():
    character_list = Character.query.filter_by(
        id_user=current_user.id_user).all()
    character_dict = {}
    for character in character_list:
        character_dict[character.id_character] = [
            character.name, character.class_name.class_name, character.racial_group.racial_group, character.level
        ]
    print(character_dict)
    return render_template('charlist.html', name=current_user.username, character_dict=character_dict)


@app.route("/create-char.html", methods=("POST", "GET"))
@login_required
def create_char():
    if request.method == "POST":
        id_user = current_user.id_user
        name_ch = request.form.get('name_ch')
        racial_group = request.form.get('race')
        result = RacialGroup.query.filter_by(racial_group=racial_group).first()
        id_racial_group = result.id_racial_group
        class_name = request.form.get('class')
        result2 = Class.query.filter_by(class_name=class_name).first()
        id_class = result2.id_class
        level = request.form.get('level')
        strength = request.form.get('strength')
        dexterity = request.form.get('dexterity')
        constitution = request.form.get('constitution')
        intelect = request.form.get('intelect')
        wisdom = request.form.get('wisdom')
        charisma = request.form.get('charisma')
        answers = request.form.getlist('answer1')
        equipments = request.form.getlist('answer2')

        text = ''
        for equipment in equipments:
            text = text + equipment + '\n'
        new_note = Note(text=text)
        db.session.add(new_note)
        db.session.flush()
        note_id = new_note.id_note

        health_max = 7 + int(constitution) * 3
        new_character = Character(name=name_ch, level=level, strength=strength, dexterity=dexterity, constitution=constitution,
                                  intelligence=intelect, wisdom=wisdom, charisma=charisma, armor_class=10, speed=30,
                                  initiative=dexterity, health_current=health_max, health_max=health_max,
                                  proficiency_bonus=0, inspiration=0, id_attack=0, id_note=note_id, id_class=id_class,
                                  id_racial_group=id_racial_group, id_user=current_user.id_user)
        db.session.add(new_character)
        db.session.flush()
        id_character = new_character.id_character

        for answer in answers:
            result3 = Proficiency.query.filter_by(proficiency=answer).first()
            id_proficiency = result3.id_proficiency
            new_ch_proficiency = CharacterProficiency(
                checker=True, id_proficiency=id_proficiency, id_character=id_character)
            db.session.add(new_ch_proficiency)
            db.session.flush()

        for equipment in equipments:
            result4 = Equipment.query.filter_by(equipment=equipment).first()
            id_equipment = result4.id_equipment
            new_ch_equipment = CharacterEquipment(
                checker=True, id_equipment=id_equipment, id_character=id_character)
            db.session.add(new_ch_equipment)
            db.session.flush()

        db.session.commit()
        return redirect(url_for("charlist"))
    return render_template("create-char.html", name=current_user.username)


@app.route("/dice.html")
def dice():
    return render_template("dice.html")


@app.route("/character/<id_class_f>")
@login_required
def character(id_class_f):
    character_obj = Character.query.filter_by(id_character=id_class_f).first()

    if character_obj is None:
        abort(404)
    character_dict = {
        'name': character_obj.name, 
        'level': character_obj.level, 
        'class_name': character_obj.class_name.class_name, 
        'racial_group': character_obj.racial_group.racial_group, 
        'strength': character_obj.strength,
        'dexterity': character_obj.dexterity,
        'constitution': character_obj.constitution,
        'intelligence': character_obj.intelligence,
        'wisdom': character_obj.wisdom,
        'charisma': character_obj.charisma,
        'armor_class': character_obj.armor_class,
        'speed': character_obj.speed,
        'initiative': character_obj.initiative,
        'health_current': character_obj.health_current,
        'health_max': character_obj.health_max,
        'proficiency_bonus': character_obj.proficiency_bonus,
        'inspiration': character_obj.inspiration,
        'attack': character_obj.attack.name,
        'note': character_obj.note.text,
    }
    print(character_dict)
    
    return render_template("character.html", character=character_dict, name=current_user.username)



@app.route('/auth.html', methods=("POST", "GET"))
def auth():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Логін або пароль введено невірно')
            return redirect(url_for('auth'))
        login_user(user)
        return redirect(url_for("charlist"))

    return render_template('auth.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))


@app.route("/registration.html", methods=("POST", "GET"))
def registration():
    if request.method == "POST":
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            print("Паролі не збігаються")
        else:
            try:
                hash = generate_password_hash(password)
                new_user = User(username=request.form['username'], email=request.form['email'],
                                password=hash, id_user_type=1)
                db.session.add(new_user)
                db.session.flush()
                db.session.commit()
                return redirect(url_for("auth"))
            except Exception as e:
                db.session.rollback()
                print("Помилка додавання в БД:", e)
    return render_template("registration.html")


class UserType(db.Model):
    id_user_type = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_type = db.Column(db.String(50), nullable=False)


class Class(db.Model):
    id_class = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(50), nullable=False)


class RacialGroup(db.Model):
    id_racial_group = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    racial_group = db.Column(db.String(50), nullable=False)


class Equipment(db.Model):
    id_equipment = db.Column(db.Integer, primary_key=True, autoincrement=True)
    equipment = db.Column(db.String(50), nullable=False)


class Proficiency(db.Model):
    id_proficiency = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    proficiency = db.Column(db.String(50), nullable=False)


class Note(db.Model):
    id_note = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(2000), nullable=False)


class Attack(db.Model):
    id_attack = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    attack_bonus = db.Column(db.Integer, nullable=False)
    damage_type = db.Column(db.String(100), nullable=False)


class User(UserMixin, db.Model):
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    id_user_type = db.Column(db.Integer, db.ForeignKey(
        'user_type.id_user_type'), nullable=False)
    user_type = db.relationship('UserType', backref='users')

    def get_id(self):
        return (self.id_user)


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
    proficiency_bonus = db.Column(db.Integer, nullable=False)
    inspiration = db.Column(db.Integer, nullable=False)
    id_attack = db.Column(db.Integer, db.ForeignKey(
        'attack.id_attack'), nullable=False)
    attack = db.relationship('Attack', backref='characters')
    id_note = db.Column(db.Integer, db.ForeignKey(
        'note.id_note'), nullable=False)
    note = db.relationship('Note', backref='characters')
    id_class = db.Column(db.Integer, db.ForeignKey(
        'class.id_class'), nullable=False)
    class_name = db.relationship('Class', backref='characters')
    id_racial_group = db.Column(db.Integer, db.ForeignKey(
        'racial_group.id_racial_group'), nullable=False)
    racial_group = db.relationship('RacialGroup', backref='characters')
    id_user = db.Column(db.Integer, db.ForeignKey(
        'user.id_user'), nullable=False)
    user = db.relationship('User', backref='characters')


class CharacterProficiency(db.Model):
    id_ch_proficiency = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    checker = db.Column(db.Boolean, nullable=False)
    id_proficiency = db.Column(db.Integer, db.ForeignKey(
        'proficiency.id_proficiency'), nullable=False)
    proficiency = db.relationship(
        'Proficiency', backref='character_proficiencies')
    id_character = db.Column(db.Integer, db.ForeignKey(
        'character.id_character'), nullable=False)
    character = db.relationship('Character', backref='character_proficiencies')


class CharacterEquipment(db.Model):
    id_ch_equipment = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    checker = db.Column(db.Boolean, nullable=False)
    id_equipment = db.Column(db.Integer, db.ForeignKey(
        'equipment.id_equipment'), nullable=False)
    equipment = db.relationship('Equipment', backref='character_equipments')
    id_character = db.Column(db.Integer, db.ForeignKey(
        'character.id_character'), nullable=False)
    character = db.relationship('Character', backref='character_equipments')


if __name__ == "__main__":
    print('Сайт Працуэ')
    app.run(debug=True)


# from main import app, db
# app.app_context().push()
# db.create_all()
# exit()`
