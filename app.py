from flask import Flask,request, render_template, session, url_for
import flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select 

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

def create_blog(title, body):
    newblog = Blog(title, body)
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

def get_posts():
    blogs = []
    with app.app_context():
        id_list = (db.session.query(Blog.id).all())
        id_count = len(id_list)
        #query = "SELECT id FROM blog"
        #result = int(db.engine.execute(query))
        for i in range(id_count):
            query = "SELECT title FROM blog WHERE id=" + str(i)
            post_title = str(db.engine.execute(query))
            query = "SELECT body FROM blog WHERE id=" + str(i)
            post_body = str(db.engine.execute(query))
            blog_post = post_title + post_body
            blogs.append(blog_post)
        return blogs

@app.route("/")
def index():
    return flask.redirect(url_for("blog"))

@app.route("/blog")
def blog():
    blogs = get_posts()
    display_posts = ""
    for blog in blogs:
        #post = """<h1>""" + post + """</h1>"""
        display_posts += blog
    return render_template("blog.html",
    post = display_posts)

@app.route('/newpost')
def newpost():
    return render_template("blogform.html")

@app.route('/newpost',methods=["POST"])
def add_blog():
    blog_title = request.form['title']
    blog_body = request.form['body']
    if blog_title == "" or blog_title == " ":
        feedback_message = "Please enter a title for your blog."
        if blog_body == "" or blog_body == " ":
            feedback_message = "Please enter a title for you blog and enter a body."
        return render_template("blogform.html",
        title = blog_title,
        body = blog_body,
        feedback = feedback_message)

    if blog_body == "" or blog_body == " ":
        feedback_message = "Please enter a body."
        return render_template("blogform.html",
        title = blog_title,
        body = blog_body,
        feedback = feedback_message)
    
    else:
        create_blog(blog_title, blog_body)
        return flask.redirect(url_for("blog"))

app.run()
#if __name__ == '__app__':
    