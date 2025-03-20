import csv
import io
from pathlib import Path
import sys
import webbrowser

import tidalapi
import yaml
from flask import Flask, redirect, render_template, url_for, request
from tidal_favorites import TidalFavoritesManager  # Import your class

app = Flask(__name__)

global tidal_session
tidal_favorites_manager = None


def open_tidal_session(config=None):
    try:
        with open('.session.yml', 'r') as session_file:
            previous_session = yaml.safe_load(session_file)
    except OSError:
        previous_session = None

    if config:
        session = tidalapi.Session(config=config)
    else:
        session = tidalapi.Session()
    if previous_session:
        try:
            if session.load_oauth_session(token_type=previous_session['token_type'],
                                          access_token=previous_session['access_token'],
                                          refresh_token=previous_session['refresh_token']):
                return session
        except Exception as e:
            print("Error loading previous Tidal Session: \n" + str(e))

    login_data, future = session.login_oauth()
    print('Login with the webbrowser: ' + login_data.verification_uri_complete)
    url = login_data.verification_uri_complete
    if not url.startswith('https://'):
        url = 'https://' + url
    webbrowser.open(url)
    future.result()
    with open('.session.yml', 'w') as f:
        yaml.dump({'session_id': session.session_id,
                   'token_type': session.token_type,
                   'access_token': session.access_token,
                   'refresh_token': session.refresh_token}, f)
    return session


# run this when the page first loads
@app.route('/')
def index():
    return render_template('index.html')


# run this when the user clicks the login button
@app.route('/login', methods=['GET', 'POST'])
def login():
    global tidal_session

    tidal_session = open_tidal_session()

    if not tidal_session.check_login():
        sys.exit("Could not connect to Tidal")

    return "Login successful"


@app.route('/post_login')
def post_login():
    global tidal_session, tidal_favorites_manager
    tidal_favorites_manager = TidalFavoritesManager(tidal_session)

    tracks = tidal_session.user.favorites.tracks()
    albums = tidal_session.user.favorites.albums(),
    videos = tidal_session.user.favorites.videos(),
    artists = tidal_session.user.favorites.artists(),
    playlists = tidal_session.user.favorites.playlists(),

    flat_albums = [item for sublist in albums for item in sublist] if albums and isinstance(
        albums[0], list) else albums
    flat_artists = [item for sublist in artists for item in sublist] if artists and isinstance(
        artists[0], list) else artists
    flat_videos = [item for sublist in videos for item in sublist] if videos and isinstance(
        videos[0], list) else videos
    flat_playlists = [item for sublist in playlists for item in sublist] if playlists and isinstance(
        playlists[0], list) else playlists

    return render_template('post_login.html',
                           tracks=tracks,
                           albums=flat_albums,
                           artists=flat_artists,
                           videos=flat_videos,
                           playlists=flat_playlists)


@app.route('/import_favorites', methods=['POST'])
def import_favorites():
    file = request.files['csvFile']

    # Create an in-memory file-like object from the uploaded data
    csv_stream = io.StringIO(file.stream.read().decode("UTF-8"), newline="")
    csv_reader = csv.reader(csv_stream)

    errors = tidal_favorites_manager.upload_favorites(
        csv_reader, file.filename)  # Pass the reader directly

    if errors:
        return f"Errors during import: {', '.join(errors)}"
    else:
        return "Favorites imported successfully!"


@app.route('/export_favorites', methods=['GET'])
def export_favorites():
    tidal_favorites_manager.download_favorites()
    return "Favorites saved!"

# @app.route('/import_favorites')
# def import_favorites():
#     favorites = session_main.get_user_favorites_tracks()

#     # Store or process the favorites as needed
#     return "Favorites imported!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
