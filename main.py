from flask import Flask, render_template, url_for, request, make_response

app = Flask(__name__, template_folder='templates')

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
    return render_template('index_login.html', title="Страница Входа", header = "Страница входа", Subtitle = "Вход в аккаунт")


if __name__=="__main__":
    app.run(debug=True)