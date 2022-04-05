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


@app.route('/artist/<artist_name>')
def artist(artist_name: str):
    artist_data = user_data.artist(artist_name)
    return json.dumps(artist_data)


@app.route('/artist/<artist_name>/album/<album_name>')
def album(artist_name, album_name):
    album_data = user_data.album(artist_name, album_name)
    return json.dumps(album_data)


@app.route('/artist/<artist_name>/song/<song_name>')
def song(artist_name, song_name):
    song_data = user_data.album(artist_name, song_name)
    return json.dumps(song_data)


if __name__ == '__main__':
    app.run()
