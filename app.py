from flask import Flask, render_template, request , redirect,url_for,flash
import sqlite3

app = Flask( __name__)
app.secret_key = "super secret key"


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    
    db=sqlite3.connect("database.db",check_same_thread=False)
    im=db.cursor()

    if request.method=="POST":
        try:
            email = request.form["email"]
            password = request.form["password"]
            im.execute("SELECT * FROM userTable WHERE email='%s' AND password='%s'" %(email,password))
            kontrol=im.fetchone()
            flash(kontrol[3])
            return redirect(url_for("login"))
        except:
            flash("email or password is wrong")
        finally:
            db.commit()
            db.close()

    return render_template("login.html")


@app.route("/register" , methods=["POST","GET"])
def register():
    
    db=sqlite3.connect("database.db",check_same_thread=False)
    im=db.cursor()

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        coniiformPass = request.form["coniiformPass"]
        if username and email and password and coniiformPass :
            if password == coniiformPass:
                im.execute("""SELECT * FROM userTable WHERE email="{}" """.format(email))
                kontrol=im.fetchone()
                if kontrol:
                    flash("{} is already exist".format(kontrol[1]))
                else:
                    try:
                        db_inputs="""INSERT INTO userTable VALUES ("%s","%s","%s","successfully signed in")"""%(username,email,password)
                        im.execute(db_inputs)
                        db.commit()
                        db.close()
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