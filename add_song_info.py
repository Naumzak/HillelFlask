import os
import sqlite3


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


def add_song_information(song_information):
    query = f"""INSERT OR IGNORE INTO song(song_name, song_text, song_year, origin_lang)
    VALUES('{song_information['song_name']}', '{song_information['song_text']}', '{song_information['song_year']}',
     '{song_information['origin_lang']}')"""
    db_request(query)


def get_song_information(song_information):
    query = f"""SELECT song_id FROM song WHERE song_name = '{song_information['song_name']}'"""
    song_id = db_request(query)[0]['song_id']
    return song_id


def add_artist_information(artist_information):
    if artist_information.get('artist_info') is not None:
        query = f"""INSERT OR IGNORE INTO artist(artist_name, artist_info)
        VALUES('{artist_information['artist_name']}', '{artist_information['artist_info']}')"""
    else:
        query = f"""INSERT OR IGNORE INTO artist(artist_name)
                VALUES('{artist_information['artist_name']}')"""
    db_request(query)


def get_artist_information(artist_information):
    query = f"""SELECT artist_id FROM artist WHERE artist_name= '{artist_information['artist_name']}'"""
    artist_id = db_request(query)[0]['artist_id']
    return artist_id


def add_album_information(album_information):
    if album_information.get('album_info') is not None:
        query = f"""INSERT OR IGNORE INTO album(album_name, album_year, album_info)
                VALUES('{album_information['album_name']}', '{album_information['album_year']}', 
                '{album_information['album_info']}')"""
    else:
        query = f"""INSERT OR IGNORE INTO album(album_name, album_year, album_info)
        VALUES('{album_information['album_name']}', '{album_information['album_year']}', 'Нет информации' )"""
    db_request(query)


def get_album_information(album_information):
    query = f"""SELECT album_id FROM album WHERE album_name= '{album_information['album_name']}'"""
    album_id = db_request(query)[0]['album_id']
    return album_id


def info_about_song(ifs):
    query = f"""INSERT OR IGNORE INTO info_about_song(artist_id, song_id, album_id)
    VALUES('{ifs['artist_id']}', '{ifs['song_id']}', '{ifs['album_id']}')"""
    db_request(query)
