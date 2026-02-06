import os
import json
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from datetime import datetime
from pathlib import Path
from thai_quiz import render_quiz

app = Flask(__name__)

USERS_FILE = Path("users.json")

def load_users():
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text())
    return {}

def save_users(users):
    USERS_FILE.write_text(json.dumps(users, indent=2))

# Secret key for sessions
app.secret_key = os.environ["SECRET_KEY"]

# OAuth setup
oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    },
)

@app.route("/")
def index():
    if "user" in session:
        u = session["user"]

        login_count = u.get("login_count", 0)
        last_login = u.get("last_login")

        msg = f"Hello {u.get('name', 'there')}<br>"
        msg += f"You have logged in {login_count} times. "

        if last_login:
            msg += f"Last login was {last_login}"

        msg += ' <a href="/logout">Logout</a><br/>'
  	# 👇 Call the quiz
        quiz_html = render_quiz()

        return msg + quiz_html

    return '<a href="/login/google">Login with Google</a>'



@app.route("/login/google")
def login_google():
    redirect_uri = url_for("auth_google", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/auth/google")
def auth_google():
    token = google.authorize_access_token()
    user = google.parse_id_token(token, nonce=token.get("nonce"))

    email = user["email"]
    name = user.get("name")

    users = load_users()
    now = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    if email in users:
        users[email]["login_count"] += 1
        last_login = users[email]["last_login"]
        users[email]["last_login"] = now
    else:
        users[email] = {
            "name": name,
            "login_count": 1,
            "last_login": now
        }
        last_login = None

    save_users(users)

    session["user"] = {
        "email": email,
        "name": name,
        "login_count": users[email]["login_count"],
        "last_login": last_login
    }

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


# jsonify(drill)


