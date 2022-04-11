from flask import Flask, request
import json
import user_data

# import requests

app = Flask(__name__)


@app.route('/search')
def search():  # put application's code here
    request_args = request.args
    search_result = user_data.search(request_args['search_string'])
    return json.dumps(search_result)


@app.route('/artist/<artist_name>', methods=['GET', 'PUT'])
def artist(artist_name: str):
    if request.method == 'GET':
        artist_data = user_data.artist(artist_name)
        return json.dumps(artist_data)
    else:
        artist_data = request.json
        user_data.update_artist(artist_name, album_name, album_data)
        return artist_data


@app.route('/artist/<artist_name>/album/<album_name>', methods=['GET', 'PUT'])
def album(artist_name, album_name):
    if request.method == 'GET':
        album_data = user_data.album(artist_name, album_name)
        return json.dumps(album_data)
    else:
        album_data = request.json
        user_data.update_album(artist_name, album_name, album_data)
        return album_data


@app.route('/artist/<artist_name>/song/<song_name>', methods=['GET', 'DELETE', 'PUT'])
def song(artist_name, song_name):
    if request.method == 'GET':
        song_data = user_data.song(artist_name, song_name)
        return json.dumps(song_data)
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
