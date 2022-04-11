import os
import sqlite3
import add_song_info


def db_request(query):
    data_base = os.environ['db_name']
    con = sqlite3.connect(data_base)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    result = [dict(i) for i in cur.fetchall()]
    cur.close()
    con.close()
    return result


def artist(artist_name):
    query = f"""
                SELECT DISTINCT al.album_name, album_year FROM album as al
                JOIN info_about_song AS ias ON ias.album_id = al.album_id
                JOIN artist as ar ON ar.artist_id = ias.artist_id
                WHERE ar.artist_name = '{artist_name.title()}'"""
    result = db_request(query)
    return result


def album(artist_name, album_name):
    query = f"""
                        SELECT DISTINCT s.song_name, s.song_text, s.origin_lang, s.song_year  FROM song as s
    JOIN info_about_song AS ias ON ias.song_id = s.song_id
    JOIN album as al ON al.album_id = ias.album_id
    JOIN artist as ar ON ar.artist_id = ias.artist_id
    WHERE ar.artist_name = '{artist_name.title()}' and al.album_name = '{' '.join(album_name.split('_')).title()}' """
    result = db_request(query)
    return result


def song(artist_name, song_name):
    query = f"""
                                SELECT DISTINCT s.song_name, s.song_text, s.origin_lang, s.song_year  FROM song as s
            JOIN info_about_song AS ias ON ias.song_id = s.song_id
            JOIN album as al ON al.album_id = ias.album_id
            JOIN artist as ar ON ar.artist_id = ias.artist_id
            WHERE ar.artist_name = '{artist_name.title()}' and s.song_name = '{' '.join(song_name.split('_')).title()}' """
    result = db_request(query)
    return result


def search(search_word):
    result = {'song': db_request(f""" SELECT song_name FROM song WHERE song_name like '%{search_word}%' """),
              'album': db_request(f""" SELECT album_name FROM album WHERE album_name like '%{search_word}%'"""),
              'artist': db_request(f""" SELECT artist_name FROM artist WHERE artist_name like '%{search_word}%'""")
              }
    return result


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
    query = f"""
                                SELECT DISTINCT s.song_id FROM song as s
            JOIN info_about_song AS ias ON ias.song_id = s.song_id
            JOIN album as al ON al.album_id = ias.album_id
            JOIN artist as ar ON ar.artist_id = ias.artist_id
            WHERE ar.artist_name = '{artist_name.title()}' and s.song_name = '{' '.join(song_name.split('_')).title()}' """

    song_id = db_request(query)[0]['song_id']
    query = f"""DELETE FROM song WHERE song_id={song_id};"""
    db_request(query)
    query = f"""DELETE FROM info_about_song WHERE song_id={song_id};"""
    db_request(query)


###################################      ОБНОВЛЕНИЕ    ###############################################

def update_song(artist_name, song_name, song_data):
    query = f"""
                                    SELECT DISTINCT s.song_id FROM song as s
                JOIN info_about_song AS ias ON ias.song_id = s.song_id
                JOIN album as al ON al.album_id = ias.album_id
                JOIN artist as ar ON ar.artist_id = ias.artist_id
                WHERE ar.artist_name = '{artist_name.title()}' and s.song_name = '{' '.join(song_name.split('_')).title()}' """

    song_id = db_request(query)[0]['song_id']
    query = f"""UPDATE song
    SET song_name = '{song_data['song_name']}', song_text ='{song_data['song_text']}', song_year = '{song_data['song_year']}', origin_lang = '{song_data['origin_lang']}'
    WHERE song_id = {song_id}"""
    db_request(query)


def update_album(artist_name, album_name, album_data):
    query = f"""
                        SELECT DISTINCT al.album_id  FROM song as s
    JOIN info_about_song AS ias ON ias.song_id = s.song_id
    JOIN album as al ON al.album_id = ias.album_id
    JOIN artist as ar ON ar.artist_id = ias.artist_id
    WHERE ar.artist_name = '{artist_name.title()}' and al.album_name = '{' '.join(album_name.split('_')).title()}' """

    album_id = db_request(query)[0]['album_id']
    query = f"""UPDATE album
    SET album_name = '{album_data['album_name']}', album_year ='{album_data['album_year']}', album_info = '{album_data['album_info']}'
    WHERE album_id = {album_id}"""
    db_request(query)


def update_artist(artist_name, artist_data):
    query = f"""SELECT DISTINCT artist_id FROM artist
    WHERE artist_name = '{artist_name.title()}' """

    artist_id = db_request(query)[0]['artist_id']
    query = f"""UPDATE artist
    SET artist_name = '{artist_data['artist_name']}', artist_info ='{artist_data['artist_info']}'
    WHERE artist_id = {artist_id}"""
    db_request(query)
