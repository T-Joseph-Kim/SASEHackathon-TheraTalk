from flask import Flask, render_template, url_for, flash, redirect, request
import secrets
import os
from PIL import Image
from flaskShell import app, db, bcrypt
from flaskShell.forms import RegistrationForm, LoginForm, UpdateForm, JournalForm
from flaskShell.models import User, Conversation, Journal
from flask_login import login_user, current_user, logout_user, login_required
from llama_index import StorageContext, load_index_from_storage
from .chatbot import Chatbot, index


from dotenv import load_dotenv
load_dotenv()

creators = [
    {
        "Name" : "Jun Tianzhong",
        "Title" : "Front-End"
    },

    {
        "Name" : "Joseph Kim",
        "Title" : "Login Feature"
    },

    {
        "Name" : "Manas Adepu", 
        "Title" : "ChatBot"
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html", creators=creators)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: 
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/journal")
@login_required
def journals():
    journals = Journal.query.all()
    return render_template("journal.html", journals=journals)

@app.route("/add_journal", methods=['GET', 'POST'])
@login_required
def add_journal():
    form = JournalForm()
    if form.validate_on_submit():
        journal = Journal(
            title=form.title.data,
            date=form.entry_date.data,
            content=form.content.data,
        )
        db.session.add(journal)
        db.session.commit()
        flash('Your journal entry has been added!', 'success')
        return redirect(url_for('journals'))
    return render_template('add_journal.html', title='Add Journal', form=form)

@app.route("/delete_journal/<int:journal_id>", methods=['POST'])
@login_required
def delete_journal(journal_id):
    journal = Journal.query.get_or_404(journal_id)
    if journal:
        db.session.delete(journal)
        db.session.commit()
        flash('Journal entry has been deleted!', 'success')
    return redirect(url_for('journals'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): 
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else: 
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


def updatePic(form_picture): 
    random_hex = secrets.token_hex(8)
    _, fileExtention = os.path.splitext(form_picture.filename)
    pictureFileName = random_hex + fileExtention
    path = os.path.join(app.root_path, "static/profile_pics", pictureFileName)
    oSize = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(oSize)
    image.save(path)  #image resizing

    return pictureFileName


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit(): 
        if form.picture.data:
            picture_file = updatePic(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account information has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/chat')
def chatUI():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    bot = Chatbot(os.environ.get("OPENAI_API_KEY"), index=index, user_id=1)
    bot.load_chat_history()
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input, bot)

def get_Chat_response(text, bot):
    
    response = bot.generate_response(text)

    return response['content']

def test_response(text):
    return "Hello!"


