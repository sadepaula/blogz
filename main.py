
from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:createablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 5
"""def css_count():
css_count = ""
css_count += 1 
return""" 
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        

    
@app.route('/blog',methods =['GET'])
def blog():
    if request.args:
        blogpost_num = request.args.get("id")
        blog = Blog.query.get(blogpost_num)
        return render_template('individualblogs.html', blog=blog)

    else:
        blogs = Blog.query.all()
        return render_template ("blog.html", blogs=blogs)


@app.route('/newblog', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        blog_id = new_blog.id
        return redirect ("/blog?id="+ str(blog_id))
    else:
        print ("Error!")
        

    return render_template('newblog.html')

@app.route ('/')
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()