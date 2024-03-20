from flask import Flask, render_template, redirect, url_for
import tidalapi
import webbrowser

app = Flask(__name__)

session_main = tidalapi.Session()
obj_main, _ = session_main.login_oauth()
url_main = obj_main.verification_uri_complete

@app.route('/')
def index():
    print(url_main)
    return render_template('index.html', url_main=url_main) 


# @app.route('/login', methods=['GET', 'POST'])
# def login():


@app.route('/import_favorites')
def import_favorites():
    favorites = session_main.get_user_favorites_tracks()

    # Store or process the favorites as needed
    return "Favorites imported!"

if __name__ == '__main__':
    app.run(debug=True)
