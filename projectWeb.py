from flask import Flask, render_template

app = Flask(__name__)

from prometheus_metrics import setup_metrics
setup_metrics(app)

@app.route('/')
def home():
    return render_template('main.html')
    
@app.route('/SpeedRacer')
def fakeDatabase():
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
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
 