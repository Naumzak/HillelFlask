import add_song_info
from models import artist as artist_model, song as song_model, album as album_model, info_about_song as ias_model
import json
from models import db


def artist(artist_name):
    result = album_model.query.join(ias_model, album_model.album_id == ias_model.album_id) \
        .join(artist_model, artist_model.artist_id == ias_model.artist_id) \
        .add_columns(album_model.album_name, album_model.album_year, album_model.album_id) \
        .filter(artist_model.artist_name == artist_name.title()).all()
    info = [dict(itm) for itm in result]
    return json.dumps(info)


def album(artist_name, album_name):
    result = song_model.query.join(ias_model, ias_model.song_id == song_model.song_id) \
        .join(album_model, album_model.album_id == ias_model.album_id) \
        .join(artist_model, artist_model.artist_id == ias_model.artist_id) \
        .add_columns(song_model.song_id, song_model.song_name, song_model.song_text, song_model.origin_lang,
                     song_model.song_year) \
        .filter(artist_model.artist_name == artist_name.title()) \
        .filter(album_model.album_name == album_name.title()).all()
    info = [dict(itm) for itm in result]
    return json.dumps(info)


def song(artist_name, song_name):
    result = song_model.query.join(ias_model, ias_model.song_id == song_model.song_id) \
        .join(album_model, album_model.album_id == ias_model.album_id) \
        .join(artist_model, artist_model.artist_id == ias_model.artist_id) \
        .add_columns(song_model.song_id, song_model.song_name, song_model.song_text, song_model.origin_lang,
                     song_model.song_year) \
        .filter(artist_model.artist_name == artist_name.title()) \
        .filter(song_model.song_name == song_name.title()).all()

    info = [dict(itm) for itm in result]
    return json.dumps(info)


def search(search_word):
    result_song = song_model.query.add_columns \
        (song_model.song_id, song_model.song_name, song_model.song_text, song_model.origin_lang, song_model.song_year) \
        .filter(song_model.song_name.like(f'%{search_word}%')).all()
    result_album = album_model.query \
        .add_columns(song_model.song_id, song_model.song_name, song_model.song_text, song_model.origin_lang,
                     song_model.song_year) \
        .filter(album_model.album_name.like(f'%{search_word}%')).all()
    result_artist = artist_model.query \
        .add_columns(album_model.album_name, album_model.album_year, album_model.album_id) \
        .filter(artist_model.artist_name.like(f'%{search_word}%')).all()
    result = {'song': [dict(itm) for itm in result_song],
              'album': [dict(itm) for itm in result_album],
              'artist': [dict(itm) for itm in result_artist]
              }
    return json.dumps(result)


###################################      ДОБАВЛЕНИЕ    ###############################################

def add_song(song_data):
    info_about_song = {'artist_id': 0, 'song_id': 0, 'album_id': 0}
    add_song_info.add_song_information(song_data['song_information'])  # Вносим данные песни
    info_about_song['song_id'] = add_song_info.get_song_information(
        song_data['song_information'])  # Получаем id песни
    if song_data.get('artist_information') is not None:  # Проверяем наличие информации об исполнителе
        for artist_info in song_data['artist_information']:
            add_song_info.add_artist_information(artist_info)  # Вносим данные исполнителя
            info_about_song['artist_id'] = add_song_info.get_artist_information(artist_info)  # Получаем id исполнителя
            if artist_info.get('album_information') is not None:  # Проверяем наличие информации об альбоме
                for album_info in artist_info['album_information']:
                    add_song_info.add_album_information(album_info)  # Вносим данные альбома
                    info_about_song['album_id'] = add_song_info.get_album_information(album_info)  # Получаем id альбома
                    add_song_info.info_about_song(info_about_song)  # Вносим все id в связывающую таблицу
            else:
                info_about_song['album_id'] = 0
                add_song_info.info_about_song(info_about_song)  # Вносим все id в связывающую таблицу, кроме album_id
    else:
        info_about_song['artist_id'] = 0
        add_song_info.info_about_song(info_about_song)  # Вносим только song_id в связывающую таблицу


###################################      УДАЛЕНИЕ    ###############################################


def delete_song(artist_name, song_name):
    song_query = song_model.query.join(ias_model, ias_model.song_id == song_model.song_id) \
        .join(artist_model, artist_model.artist_id == ias_model.artist_id).add_columns(song_model.song_id) \
        .filter(artist_model.artist_name == artist_name.title()).filter(
        song_model.song_name == song_name.title()).first()
    song_id = song_query.song_id
    song_obj = song_model.query.get(song_id)
    db.session.delete(song_obj)
    db.session.commit()


###################################      ОБНОВЛЕНИЕ    ###############################################

def update_song(artist_name, song_name, song_data):
    song_query = song_model.query.join(ias_model, ias_model.song_id == song_model.song_id) \
        .join(artist_model, artist_model.artist_id == ias_model.artist_id).add_columns(song_model.song_id) \
        .filter(artist_model.artist_name == artist_name.title()).filter(
        song_model.song_name == song_name.title()).first()
    song_id = song_query.song_id
    current_song = song_model.query.get(song_id)
    current_song.song_name = song_data['song_name']
    current_song.song_text = song_data['song_text']
    current_song.song_year = song_data['song_year']
    current_song.origin_lang = song_data['origin_lang']
    db.session.commit()


def update_album(artist_name, album_name, album_data):
    album_query = album_model.query.join(ias_model, ias_model.album_id == album_model.album_id) \
        .join(artist_model, artist_model.artist_id == ias_model.artist_id).add_columns(album_model.album_id) \
        .filter(artist_model.artist_name == artist_name.title()).filter(
        album_model.album_name == album_name.title()).first()
    album_id = album_query.song_id
    current_album = album_model.query.get(album_id)
    current_album.album_name = album_data['album_name']
    current_album.album_year = album_data['album_year']
    current_album.album_info = album_data['album_info']


def update_artist(artist_name, artist_data):
    artist_query = artist_model.query.add_columns(artist_model.artist_id) \
        .filter(artist_model.artist_name == artist_name.title())
    current_artist = artist_model.query.get(artist_query.artist_id)
    current_artist.artist_name = artist_data['artist_name']
    current_artist.artist_info = artist_data['artist_info']
    db.session.commit()
