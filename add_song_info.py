from models import artist as artist_model, song as song_model, album as album_model, info_about_song as ias_model
import json
from models import create_smth


def add_song_information(song_information):
    new_song = song_model(song_name=song_information['song_name'], song_text=song_information['song_text'],
                          song_year=song_information['song_year'], origin_lang=song_information['origin_lang'])
    create_smth(new_song)


def get_song_information(song_information):
    song_query = song_model.query.add(song_model.song_id) \
        .filter(song_model.song_name == song_information['song_name'].title()).first()
    song_id = song_query.song_id
    return song_id


def add_artist_information(artist_information):
    if artist_information.get('artist_info') is None:
        artist_information['artist_info'] = ''
    new_artist = artist_model(artist_information['artist_name'], artist_information['artist_info'])
    create_smth(new_artist)


def get_artist_information(artist_information):
    artist_query = song_model.query.add(artist_model.song_id) \
        .filter(artist_model.artist_name == artist_information['artist_name'].title()).first()
    artist_id = artist_query.song_id
    return artist_id


def add_album_information(album_information):
    if album_information.get('album_info') is None:
        album_information['album_info'] = ''
    new_album = album_model(album_information['album_name'], album_information['album_year'],
                            album_information['album_info'])
    create_smth(new_album)


def get_album_information(album_information):
    album_query = album_model.query.add(album_model.album_id) \
        .filter(album_model.album_name == album_information['album_name'].title()).first()
    album_id = album_query.album_id
    return album_id


def info_about_song(ias):
    new_ias = ias_model(ias['artist_id'], ias['song_id'], ias['album_id'])
    create_smth(new_ias)
