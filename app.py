from flask import Flask,request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Password@localhost:3306/'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

@app.route("/")
def index():
    return "<h1>Blog</h1>"

app.run()