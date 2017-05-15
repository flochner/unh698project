import os
from flask import Flask, render_template, send_from_directory
from prometheus_metrics import setup_metrics

app = Flask(__name__, static_folder='static')

setup_metrics(app)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/SpeedRacer')
def fakeSpeed_db():
    f = (
         {'name':'Speed', 'castMember':'18-year-old professional racer'},
         {'name':'Spritle', 'castMember':'Speed\'s little brother'},
         {'name':'Pops', 'castMember':'Speed\'s father'},
         {'name':'Mrs. Racer', 'castMember':'Speed\'s mother'},
        )
    o = (
         {'name':'Trixie', 'castMember':'Speed\'s girlfriend'},
         {'name':'Racer X', 'castMember':'Masked racer, and secretly, Speed\'s older brother'},
         {'name':'Chim-Chim', 'castMember':'Spritle\'s chimpanzee'},
         {'name':'Sparky', 'castMember':'Mach 5 mechanic'},
        )
    return render_template('SpeedRacer/main.html', family=f, others=o)

@app.route('/Archer')
def fakeArcher_db():
    a = (
         {'name':'Sterling Malory Archer', 'castMember':'Codename: Duchess. ISIS Field Agent. Considered the world\'s most dangerous secret agent.'},
         {'name':'Malory Duchess Archer', 'castMember':'ISIS Director. Streling Archer\'s mother.'},
         {'name':'Lana Anthony Kane', 'castMember':'ISIS Field Agent. ISIS\' top female agent and Archer\'s one-time girfriend.'},
        )
    o = (
         {'name':'Cyril Figgis', 'castMember':'ISIS Comptroller.  Also one-time boyfriend of Lana.'},
         {'name':'Cheryl/Carol/Cherlene (Gimble) Tunt', 'castMember':'Malory\'s mentally unstable assistant.'},
         {'name':'Pam Poovey', 'castMember':'ISIS Human Resources Director. Fond of bear claws.'},
         {'name':'Dr. Algernop Krieger', 'castMember':'Head of ISIS Applied Research. Questionable morals at best.'},
         {'name':'Arthur Henry Woodhouse', 'castMember':'Sterling\'s long-suffering British valet.'},
         {'name':'', 'castMember':''},
        )
    return render_template('Archer/main.html', agents=a, others=o)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
