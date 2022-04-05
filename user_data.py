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