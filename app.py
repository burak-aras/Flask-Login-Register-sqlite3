from flask import Flask, render_template, request , redirect,url_for,flash
import sqlite3

db=sqlite3.connect("database.db",check_same_thread=False)
im=db.cursor()

app = Flask( __name__)
app.secret_key = "super secret key1"


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        email = request.form["email"]
        password = request.form["password"]
        im.execute("""SELECT * FROM userTable WHERE email="{}" and password="{}" """.format(email,password))
        kontrol=im.fetchone()
        if kontrol :
            flash("successfully signed in")
            return redirect(url_for("login"))
        else:
            flash("email or password is wrong")
    return render_template("login.html")


@app.route("/register" , methods=["POST","GET"])
def register():
    if request.method == "POST":
        username = str(request.form["username"])
        email = str(request.form["email"])
        password = str(request.form["password"])
        coniiformPass = str(request.form["coniiformPass"])
        if username and email and password and coniiformPass :
            if password == coniiformPass:
                im.execute("""SELECT * FROM userTable WHERE email="{}" """.format(email))
                kontrol=im.fetchone()
                if kontrol:
                    flash("email is already exist")
                else:
                    try:
                        db_inputs="""INSERT INTO userTable VALUES ("{}","{}","{}")""".format(username,email,password)
                        im.execute(db_inputs)
                        db.commit()
                        flash("successfully signed up")
                        return redirect(url_for("login"))
                    except:
                        pass
            else:
                flash("passwords does not match")
    return render_template("register.html")



if __name__ == '__main__':
    app.debug = True
    app.run()