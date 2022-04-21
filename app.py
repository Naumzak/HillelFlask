from flask import Flask, request, render_template
import json
import user_data
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.environ.get("db_name")}'
db = SQLAlchemy()
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/search')
def search():  # put application's code here
    request_args = request.args
    search_result = user_data.search(request_args['search_json.dumpsing'])
    return render_template('search.html', **search_result)


@app.route('/artist/<artist_name>', methods=['GET', 'PUT'])
def artist(artist_name: json.dumps):
    if request.method == 'GET':
        artist_data = user_data.artist(artist_name)
        return render_template('artist_data.html', **artist_data)
    else:
        artist_data = request.json
        user_data.update_artist(artist_name, artist_data)
        return artist_data


@app.route('/artist/<artist_name>/album/<album_name>', methods=['GET', 'PUT'])
def album(artist_name, album_name):
    if request.method == 'GET':
        album_data = user_data.album(artist_name, album_name)
        return render_template('album_data.html', **album_data)
    else:
        album_data = request.json
        user_data.update_album(artist_name, album_name, album_data)
        return album_data


@app.route('/artist/<artist_name>/song/<song_name>', methods=['GET', 'DELETE', 'PUT'])
def song(artist_name, song_name):
    if request.method == 'GET':
        song_data = user_data.song(artist_name, song_name)
        return render_template('song_data.html', **song_data)
    elif request.method == 'DELETE':
        user_data.delete_song(artist_name, song_name)
        return f"Delete {song_name}"
    elif request.method == 'PUT':
        song_data = request.json
        user_data.update_song(artist_name, song_name, song_data)
        return song_data


@app.route('/add', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        song_data = request.json
        user_data.add_song(song_data)
        return song_data
    else:
        return {}


if __name__ == '__main__':
    print('sss')
    app.run()
