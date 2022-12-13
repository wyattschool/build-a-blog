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

#Get the total count of ids in the database blog table.
def get_post_total():
    blog_ids = []
    with app.app_context():
        blogs = (db.session.query(Blog.id).all())
        for row in blogs:
            blog_id = str(row["id"])
            blog_ids.append(blog_id)
        post_total = len(blog_ids)
        return post_total

#Take input, create object, and add it to the database.
def create_blog(title, body):
    newblog = Blog(title, body)
    alter_database(newblog)

#Take input object and add it to the database.
def alter_database(object):
    with app.app_context():
        try:
            db.session.add(object)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

#Get all the post titles and bodies in the table.
def get_posts():
    blog_output = []
    with app.app_context():
        #Query the database for all the titles and bodies in the table.
        blogs = (db.session.query(Blog.title,Blog.body).all())
        for row in blogs:
            blog_title = str(row["title"])
            blog_output.append(blog_title)
            blog_body = str(row["body"])
            blog_output.append(blog_body)
        return blog_output

#Reroute all of requests to to /blog.
@app.route("/")
def index():
    return flask.redirect(url_for("blog"))

#Display all posts or single post
@app.route("/blog",methods=["GET"])
def blog():
    if request.args.get('id'):
        id = int(request.args.get('id'))
        #If the id provided is more than the ids in the database or equal to 0 reroute it to /blog.
        if id > get_post_total() or id == 0:
            return flask.redirect(url_for("blog"))
        #If the id provided is good look up the post
        else:
            with app.app_context():
                print("Query for the singel post.")
                #Query the database for the post's title and body based on the id in the URL.
                blogs = (db.session.query(Blog.title,Blog.body).filter(Blog.id == id))
                for row in blogs:
                    blog_title = str(row["title"])
                    blog_body = str(row["body"])
                    print(blog_title)
            #Return the single post to user
            return render_template("post.html",
            title = blog_title,
            body = blog_body)
    #Display all the posts
    else:
        blogs = get_posts()
        titles = []
        bodies = []
        i = 0
        for blog in blogs:
            mod = i % 2
            #Get every even item in the list and add it to the list of blog bodies.
            if mod > 0:
                bodies.append(blog)
                i += 1
            #Get every odd item in the list and add it to the list of blog titles.
            else:
                titles.append(blog)
                i += 1
        #Return all of the posts to user
        return render_template("blog.html",
        titlesLen = len(titles),
        titles = titles,
        bodies = bodies)

#Render a form to create a new post.
@app.route('/newpost')
def newpost():
    return render_template("blogform.html")

#Take the form input check it, provide feedback if needed about form input, and submit the input to database.
@app.route('/newpost',methods=["POST"])
def add_blog():
    need_title = "Please enter a title for your blog."
    need_body = "Please enter a body."
    blog_title = request.form['title']
    blog_body = request.form['body']
    #If title input is empty provide feedback.
    if blog_title == "" or blog_title == " ":
        feedback_message = need_title
        #If title and body input is empty provide feedback.
        if blog_body == "" or blog_body == " ":
            feedback_message = "Please enter a title for you blog and enter a body."
            return render_template("blogform.html",
        title = blog_title,
        needTitle = need_title,
        body = blog_body,
        needBody = need_body,
        feedback = feedback_message)
        else:
            return render_template("blogform.html",
        title = blog_title,
        needTitle = need_title,
        body = blog_body,
        feedback = feedback_message)

    #If body input is empty provide feedback.
    if blog_body == "" or blog_body == " ":
        feedback_message = need_body
        return render_template("blogform.html",
        title = blog_title,
        body = blog_body,
        needBody = need_body,
        feedback = feedback_message)
    
    #If the input looks good commit create the database entry and reroute to page showing the new post
    else:
        create_blog(blog_title, blog_body)
        new_post = "blog" + str(get_post_total())
        return flask.redirect((new_post))

app.run()
#if __name__ == '__app__':