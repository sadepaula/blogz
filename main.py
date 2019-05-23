
from flask import Flask, request, redirect, render_template, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:createablog@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 5
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id= db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))  
    blogs = db.relationship('Blog', backref='owner') 

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods= ['POST', 'GET'])
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash ("Logged In")

            return redirect('/blog')
        else:
            flash('User password error or user does not exist', 'error')

    return render_template('login.html')

@app.route('/signup',methods= ['POST', 'GET']) 
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        
        usernameError= ""
        password1Error= ""
        verifyError = ""

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/blog')
        else:
            return "<h1> User Exists </h1>"


    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

@app.route('/blog',methods =['GET'])
def blog():
    blogpost_num = request.args.get("id")
    blog_user = request.args.get("user")
    if blogpost_num:
        
        blog = Blog.query.get(blogpost_num)
        return render_template('individualblogs.html', blog=blog)
    
    if blog_user:
        user = User.query.get(blog_user)
        blogs_of_user = Blog.query.filter_by(owner=user)
    
        return render_template ("singleUser.html", blogs=blogs_of_user)
    else:
        blogs = Blog.query.all()
        return render_template ("blog.html", blogs=blogs)
    
@app.route('/newblog', methods=['POST', 'GET'])
def newpost():
    owner = User.query.filter_by(username= session['username']).first()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body, owner)
        db.session.add(new_blog)
        db.session.commit()
        blog_id = new_blog.id
        return redirect ("/blog?id="+ str(blog_id))
    else:
        print ("Error!")

    return render_template('newblog.html')

@app.route ('/index')
def index():
    users = User.query.all()  
    return render_template('index.html', users=users)

@app.route('/')
def home():
    return redirect ("/index")

if __name__ == '__main__':
    app.run()