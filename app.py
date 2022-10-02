import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from numpy import append
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from more import apology, login_required
from werkzeug.utils import secure_filename

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure SQLite database
db = SQL("sqlite:///fighters.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET"])
@login_required
def index():
    match = False
    index= 0
    usersSize= db.execute("SELECT COUNT(*) AS count FROM users")
    size = usersSize[0]['count']
    while match == False and index < size:
        fighters= db.execute("SELECT * FROM users WHERE (NOT id= ?) AND (id NOT IN (SELECT user_2 FROM matches WHERE user_1=?)) LIMIT 1 OFFSET ?", session["user_id"], session["user_id"], index)
        if len(fighters)==0:
            return render_template("index.html", fighter=None)
        fighter=fighters[0]
        interests= db.execute("SELECT * FROM interests WHERE id IN (SELECT interest_id FROM users_interest WHERE user_id = ?)",fighter['id'])
        myinterests= db.execute("SELECT * FROM interests WHERE id IN (SELECT interest_id FROM users_interest WHERE user_id = ?)",session["user_id"])
        match= interest_match(interests, myinterests)
        print(fighter, match)
        index+=1
    return render_template("index.html", fighter=fighter, interests=interests)

def interest_match(interests1, interests2):
    for interest1 in interests1:
        for interest2 in interests2:
            if interest1['id'] == interest2['id']:
                return True
    return False

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect('/')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Ensure username was submitted
        name = request.form.get("name")

        if not name:
            return apology("must provide a name", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure passwords match
        if request.form.get("password") != request.form.get("repeat password"):
            return apology("passwords don't match", 400)

        # Query database for email
        email = request.form.get("email")
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)

        # Check if username already exists
        if len(rows) != 0 :
            return apology("email already exists, try a different one", 400)

        psw=request.form.get("password")
        psw = generate_password_hash(psw)

        country= request.form.get("country")
        city= request.form.get("city")
        file = request.files.get('file', None)
        filename = "avatar.jpg"
        if file:
            filename = secure_filename(file.filename)
            file.save("./static/"+filename)

        newUser=db.execute("INSERT INTO users (email, hash, name, country, city, avatar) VALUES (?, ?, ?, ?, ?, ?)", email, psw, name, country, city, filename)
        interests=request.form.getlist('interests[]')
        insertInterests="INSERT INTO users_interest (user_id, interest_id) VALUES "
        for index, interest in enumerate(interests):
            insertInterests+=f"('{newUser}' , '{interest}')"
            if(len(interests)-1!=index):
                insertInterests+=","
        print("insertInterests")
        print(insertInterests)
        db.execute(insertInterests)
        return redirect("/")

    else:
        return render_template("login_register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":

        #Ensure name was submitted
        email = request.form.get("email")
        if not email:
            return apology("must provide an email", 400)

        # Ensure password was submitted
        password= request.form.get("password")
        if not password:
            return apology("must provide a password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) == 0 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["name"]
        session["user"] = rows[0]
        return redirect("/")

    else:
        return render_template("login_register.html")

@app.route("/no", methods=["POST"])
@login_required
def no():
    cuser=session["user_id"]
    cfighter=request.form.get("fighterid")
    insertStatus=f"INSERT INTO matches (user_1, user_2, status) VALUES ('{cuser}', '{cfighter}', '{False}')"
    db.execute(insertStatus)
    return redirect("/")

@app.route("/yes", methods=["POST"])
@login_required
def yes():
    cuser=session["user_id"]
    cfighter=request.form.get("fighterid")
    insertStatus=f"INSERT INTO matches (user_1, user_2, status) VALUES ('{cuser}', '{cfighter}', '{True}')"
    db.execute(insertStatus)
    return redirect("/")

@app.route("/chat", methods=["GET"])
@login_required
def chat():
    connectedQuery=f"SELECT user_2 FROM matches WHERE (status='True') AND user_2 IN (SELECT user_1 FROM matches WHERE user_2={session['user_id']} AND status='True')"
    connectedQuery=f"SELECT * FROM users WHERE id IN ({connectedQuery})"
    users=db.execute(connectedQuery)
    return render_template("chat.html", users=users)

@app.route("/msg/<user_id>", methods=["GET", "POST"])
@login_required
def msg(user_id):
    if request.method == "GET":
        connectedQuery=f"SELECT user_2 FROM matches WHERE (status='True') AND user_2 IN (SELECT user_1 FROM matches WHERE user_2={session['user_id']} AND status='True')"
        connectedQuery=f"SELECT * FROM users WHERE id IN ({connectedQuery})"
        users=db.execute(connectedQuery)
        msgsQuery=f"SELECT * FROM messages WHERE (user_from={session['user_id']} AND user_to={user_id}) OR (user_to={session['user_id']} AND user_from={user_id})"
        messages=db.execute(msgsQuery)
        return render_template("chat.html", users=users, messages=messages, tuser=user_id)
    else:
        msg=request.form.get("msg")
        cuser=session['user_id']
        db.execute('INSERT INTO "messages" ("text","user_from","user_to") VALUES (?, ?, ?)', msg, cuser,user_id)
        return redirect(f"/msg/{user_id}")
