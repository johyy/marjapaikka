from flask import render_template, request, redirect
from app import app
import users
import additions
import reviews

@app.route("/")
def index():
    list = additions.get_list()
    return render_template("index.html", additions=list)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    borough = request.form["borough"]
    genre = request.form["genre"]
    coordinates = request.form["coordinates"]
    if borough == "" or genre == "" or coordinates == "":
        return render_template("new.html")
    if additions.send(borough, genre, coordinates):
        return redirect("/")
    return render_template("error.html", message="Lisäys ei onnistunut")

@app.route("/show_review/<int:addition_id>")
def show_review(addition_id):
    print(addition_id)
    info = additions.get_addition_info(addition_id)
    reviews = additions.get_reviews(addition_id)

    return render_template("review.html", id=addition_id, borough=info[0], genre=info[1], creator=info[2], reviews=reviews)

@app.route("/review", methods=["post"])
def review():
    addition_id = request.form["addition_id"]

    stars = int(request.form["stars"])
    if stars < 1 or stars > 5:
        return render_template("error.html", message="Virheellinen tähtimäärä")

    comment = request.form["comment"]
    if len(comment) > 1000:
        return render_template("error.html", message="Kommentti on liian pitkä")
    if comment == "":
        comment = "-"

    additions.add_review(addition_id, stars, comment, users.user_id())

    return redirect("/show_review/"+str(addition_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-20 merkkiä")
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä")
        if not users.register(username, password1):
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        return redirect("/")

@app.route("/remove", methods=["get", "post"])
def remove():
    users.require_role(1)

    if request.method == "GET":
        all_additions = additions.get_list()
        return render_template("remove_addition.html", list=all_additions)

    if request.method == "POST":
        users.check_csrf()
        if "addition" in request.form:
            addition = request.form["addition"]
            additions.remove_addition(addition, users.user_id())

    return redirect("/")

@app.route("/remove_addition", methods=["get", "post"])
def remove_addition():
    if request.method == "GET":
        my_additions = additions.get_my_additions(users.user_id())
        return render_template("remove_addition.html", list=my_additions)

    if request.method == "POST":
        users.check_csrf()

    if "addition" in request.form:
        addition = request.form["addition"]
        additions.remove_addition(addition, users.user_id())
    return redirect("/")
    
@app.route("/remove_review", methods=["get", "post"])
def remove_review():
    users.require_role(1)

    if request.method == "GET":
        all_reviews = reviews.get_list()
        return render_template("remove_review.html", list=all_reviews)

    if request.method == "POST":
        users.check_csrf()
        if "review" in request.form:
            review = request.form["review"]
            reviews.remove_review(id)
            
    return redirect("/")
