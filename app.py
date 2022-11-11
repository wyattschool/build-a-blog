from flask import Flask,request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:w-myOfx)7oYPYtCA@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

def create_blog():
    print("What is the blog's name?")
    blogname = input()
    print("Enter the body to the blog. (Less than 1000 characters)")
    body = input()
    newblog = Blog(blogname, body)
    alter_database(newblog)

def alter_database(object):
    with app.app_context():
        try:
            db.session.add(object)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

@app.route("/")
def index():
    return "<h1>Blog</h1>"

@app.route("/blog")
def blog():
    return "Blogs"

if __name__ == '__app__':
    app.run()