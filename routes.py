from app import app
from flask import render_template, request, redirect
import users, additions, reviews

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
	if additions.send(borough, genre, coordinates):
		return redirect("/")
	else:
		return render_template("error.html", message="Lisäys ei onnistunut")	
		
@app.route("/show_review/<int:addition_id>")
def show_review(addition_id):
	reviews = reviews.get_reviews(addition_id)

	return render_template("review.html")

@app.route("/review", methods=["post"])
def review():
    users.check_csrf()

    addition_id = request.form["addition_id"]

    stars = int(request.form["stars"])
    if stars < 1 or stars > 5:
        return render_template("error.html", message="Virheellinen tähtimäärä")

    comment = request.form["comment"]
    if len(comment) > 1000:
        return render_template("error.html", message="Kommentti on liian pitkä")
    if comment == "":
        comment = "-"

    addition.add_review(addition_id, users.user_id(), stars, comment)

    return redirect("/show_review/"+str(deck_id))

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
		return redirect ("/")


	
		
