from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
pics_lst = ["test1"]

@app.route('/')
def home():
    return render_template('home.html', pics=pics_lst)

