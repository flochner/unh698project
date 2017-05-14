from flask import Flask, render_template
from prometheus_metrics import setup_metrics

app = Flask(__name__)

setup_metrics(app)

@app.route('/')
def home():
    return render_template('main.html')
       
if __name__ == '__main__':
    app.run(host='0.0.0.0')
 