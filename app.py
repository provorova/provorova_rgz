from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, render_template, session, request
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2

from Db import db
from Db.models import users
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

app = Flask(__name__)

app.secret_key ="123"
user_db = "provorova_rgz_orm"
host_ip = "127.0.0.1"
host_port = "5432"
database_name = "rgz_orm"
password = "123"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()

login_manager.login_view = "app.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_users(user_id):
    return users.query.get(int(user_id))

@app.route("/")
@app.route("/index")
def start():
    return redirect ("/glavn", code = 302)

@app.route('/glavn')
def glavn():
    return render_template('glavn.html')

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        username_form = request.form.get("loginuser")
        password_form = request.form.get("password")
        username = request.form.get("username")
        userage = request.form.get("userage")
        gender = request.form.get("gender")
        gender_poisk = request.form.get("gender_poisk")
        info = request.form.get("info")
        gender = request.form.get("gender")

        if username_form == '' or password_form == '':
            errors = "Пожалуйста, заполните все поля"
            return render_template("register.html", errors=errors)

        if len(password_form) < 5:
            errors = "Пароль не должен быть меньше 5-ти символов"
            return render_template("register.html", errors=errors)
        
        if (username or userage or gender or gender_poisk or info or foto) =='':
            errors = "Пожалуйста, зполните все поля анкеты"
            return render_template("register.html", errors=errors)

        isUserExist = users.query.filter_by(loginuser=username_form).first()

        if isUserExist is not None:
            errors = 'Пользватель с таким именем уже существует'
            return render_template("register.html", errors=errors)

        hashedPswd = generate_password_hash(password_form, method='pbkdf2')

        newUser = users(loginuser=username_form, password=hashedPswd, 
        username=username, userage=userage, gender=gender, 
        gender_poisk=gender_poisk, info=info)

        db.session.add(newUser)

        db.session.commit()

        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    username_form = request.form.get("loginuser")
    password_form = request.form.get("password")

    if username_form == '' or password_form == '':
        errors = "Пожалуйста, заполните все поля"
        return render_template("login.html", errors=errors)

    my_user = users.query.filter_by(loginuser=username_form).first()

    if my_user is not None:
        if check_password_hash(my_user.password, password_form):
            login_user(my_user, remember=False)
            return redirect("/profile")
        else:
            errors = "Неправильный пароль"
            return render_template("login.html", errors=errors)
    else:
        errors = "Пользователь не сущетсвует"
        return render_template("login.html", errors=errors)

@app.route("/profiles")
@login_required
def profiles():
    visibleUser = current_user.username
    result = (
        db.session.query(users.username, users.userage, users.info)
        .filter(users.is_public == True)
        .filter(users.gender == current_user.gender_poisk)
        .filter(users.gender_poisk == current_user.gender)
        .all()
    )
    return render_template("profiles.html", visibleUser=visibleUser, result=result)


@app.route("/profile")
@login_required
def profile():
    visibleUser = current_user.username
    user = users.query.filter_by(loginuser=current_user.loginuser).first()
    return render_template("profile.html", visibleUser=visibleUser, user=user)


@app.route("/publish", methods=["POST"])
def publish():
    user = users.query.filter_by(loginuser=current_user.loginuser).first()

    user.is_public = not user.is_public
    db.session.commit()

    return redirect("/profile")


@app.route("/delete")
def delete():
    user_to_delete = User.query.filter_by(loginuser=current_user.loginuser).first()
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect("/register")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")