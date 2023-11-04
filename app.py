from flask import Flask, redirect
import tidalapi

app = Flask(__name__)

@app.route('/')
def index():
    return '<a href="/login">Login with Tidal</a>'

@app.route('/login')
def login():
    session_main = tidalapi.Session()
    obj_main, _ = session_main.login_oauth()
    url_main = obj_main.verification_uri_complete
    return redirect(url_main)

if __name__ == '__main__':
    app.run(debug=True)
