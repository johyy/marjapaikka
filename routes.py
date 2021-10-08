from flask import render_template, request, redirect
from app import app
import users
import additions
import reviews
import sales
import purchases

@app.route("/")
def index():
    list = additions.get_list()
    return render_template("index.html", additions=list)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/fleamarket")
def fleamarket():
    return render_template("fleamarket.html")

@app.route("/for_sale")
def for_sale():
    list = sales.get_sales()
    return render_template("sales.html", sales=list)

@app.route("/new_sale")
def new_sale():
    return render_template("new_sale.html")

@app.route("/send_sales_ad", methods=["POST"])
def send_sales_ad():
    comment = request.form["comment"]
    borough = request.form["borough"]
    if comment == "" or borough == "":
        return render_template("new_sale.html")
    if sales.send_sales_ad(comment, borough):
        return redirect("/for_sale")
    return render_template("error.html", message="Lisäys ei onnistunut")

@app.route("/remove_sale", methods=["get", "post"])
def remove_sale():
    if request.method == "GET":
        my_sales = sales.get_my_sales(users.user_id())
        return render_template("remove_sale.html", list=my_sales)
    if request.method == "POST":
        users.check_csrf()
    if "sale" in request.form:
        sale = request.form["sale"]
        sales.remove_sale(sale, users.user_id())
    return redirect("/for_sale")

@app.route("/remove_sale_admin", methods=["get", "post"])
def remove_sale_admin():
    if request.method == "GET":
        all_sales = sales.get_sales()
        return render_template("remove_sale_admin.html", list=all_sales)
    if request.method == "POST":
        users.check_csrf()
    if "sale" in request.form:
        sale = request.form["sale"]
        sales.remove_sale_admin(sale)
    return redirect("/for_sale")

@app.route("/for_purchase")
def for_purchase():
    list = purchases.get_purchases()
    return render_template("purchases.html", purchases=list)

@app.route("/new_purchase")
def new_purchase():
    return render_template("new_purchase.html")

@app.route("/send_purchases_ad", methods=["POST"])
def send_purchases_ad():
    comment = request.form["comment"]
    borough = request.form["borough"]
    if comment == "" or borough == "":
        return render_template("new_purchase.html")
    if purchases.send_ad(comment, borough):
        return redirect("/for_purchase")
    return render_template("error.html", message="Lisäys ei onnistunut")

@app.route("/remove_purchase", methods=["get", "post"])
def remove_purchase():
    if request.method == "GET":
        my_purchases = purchases.get_my_purchases(users.user_id())
        return render_template("remove_purchase.html", list=my_purchases)
    if request.method == "POST":
        users.check_csrf()
    if "purchase" in request.form:
        purchase = request.form["purchase"]
        purchases.remove_purchase(purchase, users.user_id())
    return redirect("/for_purchase")

@app.route("/remove_purchase_admin", methods=["get", "post"])
def remove_purchase_admin():
    if request.method == "GET":
        all_purchases = purchases.get_purchases()
        return render_template("remove_purchase_admin.html", list=all_purchases)
    if request.method == "POST":
        users.check_csrf()
    if "purchase" in request.form:
        purchase = request.form["purchase"]
        purchases.remove_purchase_admin(purchase)
    return redirect("/for_purchase")

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
    info = additions.get_addition_info(addition_id)
    reviewslist = reviews.get_reviews(addition_id)
    return render_template("review.html", id=addition_id, borough=info[0], genre=info[1], creator=info[2], reviews=reviewslist)

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
    reviews.add_review(addition_id, stars, comment, users.user_id())
    return redirect("/show_review/"+str(addition_id))

@app.route("/remove_review", methods=["get", "post"])
def remove_review():
    users.require_role(1)
    addition_id = request.form["addition_id"]
    print(addition_id)
    if request.method == "GET":
        all_reviews = reviews.get_reviews(addition_id)
        return render_template("remove_review.html", list=all_reviews)
    if request.method == "POST":
        users.check_csrf()
        if "review" in request.form:
            review = request.form["review"]
            reviews.remove_review(review)
    return redirect("/")

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

@app.route("/remove_addition_admin", methods=["get", "post"])
def remove():
    users.require_role(1)
    if request.method == "GET":
        all_additions = additions.get_list()
        return render_template("remove_addition_admin.html", list=all_additions)
    if request.method == "POST":
        users.check_csrf()
        if "addition" in request.form:
            addition = request.form["addition"]
            additions.remove_addition_admin(addition)
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

@app.route("/result_genre")
def result_genre():
    query = request.args["query"]
    results = additions.get_result_genre(query)
    return render_template("result.html", list=results)

@app.route("/result_borough")
def result_borough():
    query = request.args["query"]
    results = additions.get_result_borough(query)
    return render_template("result.html", list=results)

@app.route("/result_user")
def result_user():
    query = request.args["query"]
    results = additions.get_result_user(query)
    return render_template("result.html", list=results)
