import os
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

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
    # If logged in, show Hello
    if "user" in session:
        return "Hello"

    # Otherwise show login link
    return '<a href="/login/google">Login with Google</a>'

@app.route("/login/google")
def login_google():
    redirect_uri = url_for("auth_google", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/auth/google")
def auth_google():
    token = google.authorize_access_token()

    # ✅ Correct way: nonce comes from token
    user = google.parse_id_token(token, nonce=token.get("nonce"))

    session["user"] = user
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


# jsonify(drill)


