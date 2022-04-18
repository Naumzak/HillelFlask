from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy()


class album(db.Model):
    def __init__(self, album_name, album_year, album_info=''):
        self.album_name = album_name
        self.album_year = album_year
        self.album_info = album_info
    album_id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.Text, nullable=False)
    album_year = db.Column(db.Integer, nullable=False)
    album_info = db.Column(db.Text, nullable=False)


class artist(db.Model):
    def __init__(self, artist_name, artist_info):
        self.artist_name = artist_name
        self.artist_info = artist_info
    artist_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.Text, nullable=False)
    artist_info = db.Column(db.Text, nullable=True)


class song(db.Model):
    def __init__(self, song_name, song_text, song_year, origin_lang):
        self.song_name = song_name
        self.song_text = song_text
        self.song_year = song_year
        self.origin_lang = origin_lang
    song_id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.Text, nullable=False)
    song_text = db.Column(db.Text, unique=True, nullable=False)
    song_year = db.Column(db.Integer, nullable=False)
    origin_lang = db.Column(db.Text, nullable=True)


class info_about_song(db.Model):
    def __init__(self, artist_id, album_id, song_id):
        self.album_id = artist_id
        self.album_id = album_id
        self.song_id = song_id
    table_id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, nullable=True)
    album_id = db.Column(db.Integer, nullable=True)
    song_id = db.Column(db.Integer, nullable=True)


def create_smth(obj_in):
    with app.app_context():
        db.session.add(obj_in)
        db.session.commit()