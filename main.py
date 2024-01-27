from flask import Flask, render_template, url_for, request, make_response
from db_sqllite import db, User
import os
import hashlib

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db.init_app(app)

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.get("/mainpage")
def index():
    return render_template('index.html', title="Главная страница", header="Главная страница", user_name = "Пользователь")


@app.post("/maipage")
def upload():
    if request.method == 'POST':
        f_name = request.form.get('usr_name')
        if f_name == None:
            f_name = "Пользователь"
        resp = make_response(render_template('index.html', title="Главная страница", header="Главная страница", user_name = f_name))
        resp.set_cookie("user_name", value=f_name)
        f_email = request.form.get('usr_email')
        print(f"User name: {f_name}, User email: {f_email}")
    return resp

@app.route("/about")
def about():
    return render_template('index.html', title="О нас", header="О нас")

@app.route("/contacts")
def contacts():
    return render_template('index.html', title="Контакты", header="Контакты")

@app.route("/clothes")
def clothes():
    return render_template('index_categories.html', title="Одежда", header="Одежда", Subtitle="Каталог одежды")

@app.route("/shoes")
def shoes():
    return render_template('index_categories.html', title="Обувь", header="Обувь", Subtitle="Каталог обуви")

@app.route("/login")
def login():
    return render_template('index_login.html')

@app.route("/signup")
def sign_up():
    return render_template('index_signup.html')

@app.post("/mainpage")
def add_user():
    if request.method == 'POST':
        f_name = request.form.get('usr_name')
        f_surname = request.form.get('usr_surname')
        f_email = request.form.get('usr_email')
        f_password = request.form.get('usr_password')
        f_hashed_password = hashlib.md5(f_password.encode()).hexdigest()
    user = User(username=f_name, usersurname=f_surname, email = f_email, password = f_hashed_password)
    db.session.add(user)
    db.session.commit()
    print(f"User {f_name} {f_surname} added in DB.")
    if f_name == None:
            f_name = "Пользователь"

    return render_template('index.html', title="Главная страница", header="Главная страница", user_name = f_name)


if __name__=="__main__":
    app.run(debug=True)