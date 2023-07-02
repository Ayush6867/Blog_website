import json
from post import Post
import requests
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Retrieve posts from the JSON API
response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
posts = response.json()
post_objects = []
# Create a Post object from the JSON data
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)


@app.route('/')
def get_all_posts():
    return render_template("home.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/blogs")
def blogs_page():
    return render_template("index.html", all_posts=post_objects)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("login.html", form=LoginForm())


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.email.data
        password = form.password.data
        credential = {
            "Username": username,
            "Password": password
        }
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(credential, data_file, indent=4)
            return render_template("home.html")
        else:
            data.update(credential)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
            return render_template("home.html")
    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4040)
