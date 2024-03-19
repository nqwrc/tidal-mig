from flask import Flask, render_template, redirect, url_for
import tidalapi

app = Flask(__name__)

@app.route('/')
def index():
    return '<a href="/login">Login with Tidal</a>'
    # return '<a href="/login" class="button">Login with Tidal</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    session_main = tidalapi.Session()
    obj_main, _ = session_main.login_oauth()
    url_main = obj_main.verification_uri_complete
    return redirect(url_main)

@app.route('/import_favorites')
def import_favorites():
    favorites = session.get_user_favorites_tracks()

    # Store or process the favorites as needed
    return "Favorites imported!"

if __name__ == '__main__':
    app.run(debug=True)
