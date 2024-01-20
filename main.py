from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route("/mainpage")
def index():
    return render_template('index.html', title="Главная страница", header="Главная страница")

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

if __name__=="__main__":
    app.run(debug=True)