from flask import Flask, request, redirect, url_for, render_template, session
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Secure session cookie settings
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False

bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

DATABASE = "users.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            message = "Username and password are required."

        elif len(username) < 3:
            message = "Username must contain at least 3 characters."

        elif len(password) < 8:
            message = "Password must contain at least 8 characters."

        else:
            password_hash = bcrypt.generate_password_hash(
                password
            ).decode("utf-8")

            try:
                conn = get_db_connection()

                conn.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash)
                )

                conn.commit()
                conn.close()

                return redirect(url_for("login"))

            except sqlite3.IntegrityError:
                message = "Username already exists."

    return render_template("register.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if user and bcrypt.check_password_hash(
            user["password_hash"],
            password
        ):

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(url_for("dashboard"))

        else:
            message = "Invalid username or password."

    return render_template("login.html", message=message)


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)