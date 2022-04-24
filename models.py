from flask_sqlalchemy import SQLAlchemy
import app

db = SQLAlchemy()

class album(app.db.Model):
    def __init__(self, album_name, album_year, album_info=''):
        self.album_name = album_name
        self.album_year = album_year
        self.album_info = album_info

    album_id = app.db.Column(app.db.Integer, primary_key=True)
    album_name = app.db.Column(app.db.Text, nullable=False)
    album_year = app.db.Column(app.db.Integer, nullable=False)
    album_info = app.db.Column(app.db.Text, nullable=False)


class artist(app.db.Model):
    def __init__(self, artist_name, artist_info):
        self.artist_name = artist_name
        self.artist_info = artist_info

    artist_id = app.db.Column(app.db.Integer, primary_key=True)
    artist_name = app.db.Column(app.db.Text, nullable=False)
    artist_info = app.db.Column(app.db.Text, nullable=True)


class song(app.db.Model):
    def __init__(self, song_name, song_text, song_year, origin_lang):
        self.song_name = song_name
        self.song_text = song_text
        self.song_year = song_year
        self.origin_lang = origin_lang

    song_id = app.db.Column(app.db.Integer, primary_key=True)
    song_name = app.db.Column(app.db.Text, nullable=False)
    song_text = app.db.Column(app.db.Text, unique=True, nullable=False)
    song_year = app.db.Column(app.db.Integer, nullable=False)
    origin_lang = app.db.Column(app.db.Text, nullable=True)


class info_about_song(app.db.Model):
    def __init__(self, artist_id, album_id, song_id):
        self.album_id = artist_id
        self.album_id = album_id
        self.song_id = song_id

    table_id = app.db.Column(app.db.Integer, primary_key=True)
    artist_id = app.db.Column(app.db.Integer, nullable=True)
    album_id = app.db.Column(app.db.Integer, nullable=True)
    song_id = app.db.Column(app.db.Integer, nullable=True)


def create_smth(obj_in):
    with app.app.app_context():
        app.db.session.add(obj_in)
        app.db.session.commit()
