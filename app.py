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

def get_post_total():
    blog_ids = []
    with app.app_context():
        blogs = (db.session.query(Blog.id).all())
        for row in blogs:
            blog_id = str(row["id"])
            blog_ids.append(blog_id)
        post_total = len(blog_ids)
        return post_total
        
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
    blog_output = []
    with app.app_context():
        blogs = (db.session.query(Blog.title,Blog.body).all())
        for row in blogs:
            blog_title = str(row["title"])
            blog_output.append(blog_title)
            blog_body = str(row["body"])
            blog_output.append(blog_body)
        return blog_output

@app.route("/")
def index():
    return flask.redirect(url_for("blog"))

@app.route("/blog")
def blog():
    blogs = get_posts()
    titles = []
    bodies = []
    i = 0
    for blog in blogs:
        mod = i % 2
        if mod > 0:
            bodies.append(blog)
            i += 1
        else:
            titles.append(blog)
            i += 1
        
    return render_template("blog.html",
    titlesLen = len(titles),
    titles = titles,
    bodies = bodies)

@app.route("/blog<int:id>",methods=["GET"])
def displaysingle_post(id=None):
    if id > get_post_total() or id == 0:
        return flask.redirect(url_for("blog"))
    else:
        with app.app_context():
            blogs = (db.session.query(Blog.title,Blog.body).filter(Blog.id == id))
            for row in blogs:
                blog_title = str(row["title"])
                blog_body = str(row["body"])
        return render_template("post.html",
        title = blog_title,
        body = blog_body)

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
        new_post = "blog" + str(get_post_total())
        return flask.redirect((new_post))

@app.route('/test<post_id>')
def test(post_id):
    #We want to redirect to a post with the provided id number from the url
    id = post_id
    url = "blog"+str(id)
    return flask.redirect((url))

app.run()
#if __name__ == '__app__':