from flask import Flask, render_template, url_for, send_file
import json
import os

app = Flask(__name__, static_folder='static')

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
    monster_properties= {}
    for key, value in monsters1.items():
        if (monsters_name.lower() == value[1].lower()):
            for_api_key = value[1]
            f = open(f"./static/json/all_types_details/monsters/{for_api_key}.json")
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
    return render_template("bestiary.html", dict_monster_prop = monster_properties, monsters = monsters1)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/merche.html")
def merche():
    return render_template("merche.html")

@app.route("/auth.html")
def auth():
    return render_template("auth.html")

@app.route("/registration.html")
def registration():
    return render_template("registration.html")

@app.route("/charlist.html")
def charlist():
    return render_template("charlist.html")

@app.route("/create-char.html")
def create_char():
    return render_template("create-char.html")

@app.route("/dice.html")
def dice():
    return render_template("dice.html")

@app.route("/character.html")
def character():
    return render_template("character.html")

if __name__ == "__main__":
    print('start server')
    app.run(debug=True)