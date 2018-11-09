import os
import json
import random
from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret"
app.secret_key = os.urandom(24)

"""Read userfile for registered users"""
def users():
    with open("data/users.txt", "r") as user_data:
        registered_users = user_data.read().splitlines()
        return registered_users
        
"""Start game variables"""
def start_game():
    session['question_number'] = 1
    session['players'] = generate_random_player()
    session['user_score'] = 0
    return session['question_number'], session['players'], session['user_score']
    
"""Generate Random Player Image"""
def generate_random_player():
    with open("data/players.json", "r") as players_data:
        players_list = json.load(players_data)["players"]
        random.shuffle(players_list)
        return players_list
        
"""Scores"""
def user_scores():
    with open("data/scores.json", "r") as score_data:
        data = json.load(score_data)
        return data
        
"""Routing"""

@app.route('/')
def index():
    return render_template("index.html")
    
app.route('/register')
def register():
    if session:
        return redirect(url_for("play"))
    else:
        return render_template("register.html")

@app.route('/register', methods = ["GET", "POST"])
def register_user():
    if session:
        return redirect(url_for("play"))
    else:
        if request.method == "POST":
            new_user = request.form["username"]
            registered_users = users()
            if new_user in registered_users:
                flash('This username "{}" is already taken. Please choose another'.format(request.form["username"]))
            else:
                if request.method == "POST":
                    user_list = open("data/users.txt", "a")
                    user_list.write(new_user + "\n")
                    session['user'] = new_user
                    return redirect(url_for("play"))
        return render_template("register.html")
    
@app.route('/play')
def play():
    if session:
        users()
        start_game()
        registered_users = users()
        question_number = session['question_number']
        data = session['players']
        score = session['user_score']
        return render_template("play.html", question_number=question_number, players=data, user_score=score)
    else:
        return redirect(url_for("index"))
    
    
@app.route('/leaderboard') 
def leaderboard():
    return render_template("leaderboard.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")
    
@app.route('/about')
def about():
    return render_template("about.html")

if __name__=='__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            