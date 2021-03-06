
import serializers


def artist(artist_name):
    from models import artist as artist_model, album as album_model, info_about_song as ias_model
    result = album_model.query.join(ias_model, album_model.album_id == ias_model.album_id) \
        .join(artist_model, artist_model.artist_id == ias_model.artist_id) \
        .add_columns(album_model.album_name, album_model.album_year, album_model.album_id) \
        .filter(artist_model.artist_name == artist_name.title()).all()
    info = [dict(itm) for itm in result]
    return {'info': info, 'artist_name': artist_name}


def album(artist_name, album_name):
    from models import artist as artist_model, song as song_model, album as album_model, info_about_song as ias_model
    result = song_model.query.join(ias_model, ias_model.song_id == song_model.song_id) \
        .join(album_model, album_model.album_id == ias_model.album_id) \
        .join(artist_model, artist_model.artist_id == ias_model.artist_id) \
        .add_columns(song_model.song_id, song_model.song_name, song_model.song_text, song_model.origin_lang,
                     song_model.song_year) \
        .filter(artist_model.artist_name == artist_name.title()) \
        .filter(album_model.album_name == album_name.title()).all()
    info = [dict(itm) for itm in result]
    return {'info': info, 'artist_name': artist_name, 'album_name': album_name}


def song(artist_name, song_name):
    from models import artist as artist_model, song as song_model, album as album_model, info_about_song as ias_model
    result = song_model.query.join(ias_model, ias_model.song_id == song_model.song_id) \
        .join(album_model, album_model.album_id == ias_model.album_id) \
        .join(artist_model, artist_model.artist_id == ias_model.artist_id) \
        .add_columns(song_model.song_id, song_model.song_name, song_model.song_text, song_model.origin_lang,
                     song_model.song_year, album_model.album_name) \
        .filter(artist_model.artist_name == artist_name.title()) \
        .filter(song_model.song_name == song_name.title()).all()

    info = [dict(itm) for itm in result]
    return {'info': info, 'artist_name': artist_name, 'song_name': song_name, 'album_name': info[0]['album_name']}


def search(search_word):
    from models import artist as artist_model, song as song_model, album as album_model, info_about_song as ias_model
    result_song = song_model.query.join(ias_model, ias_model.song_id == song_model.song_id) \
        .join(artist_model, artist_model.artist_id == ias_model.artist_id) \
        .add_columns(artist_model.artist_name, song_model.song_name)\
        .filter(song_model.song_name.like(f'%{search_word}%')).all()
    result_album = song_model.query.join(ias_model, ias_model.song_id == song_model.song_id) \
        .join(album_model, album_model.album_id == ias_model.album_id) \
        .join(artist_model, artist_model.artist_id == ias_model.artist_id) \
        .add_columns(artist_model.artist_name, album_model.album_name)\
        .filter(album_model.album_name.like(f'%{search_word}%')).all()
    result_artist = artist_model.query \
        .add_columns(artist_model.artist_name) \
        .filter(artist_model.artist_name.like(f'%{search_word}%')).all()
    result = {'songs': [dict(itm) for itm in result_song],
              'albums': [dict(itm) for itm in result_album],
              'artists': [dict(itm) for itm in result_artist]
              }
    return {'songs': result['songs'], 'albums': result['albums'], 'artists': result['artists']}


###################################      ????????????????????    ###############################################

def add_song(song_data):
    import add_song_info
    info_about_song = {'artist_id': 0, 'song_id': 0, 'album_id': 0}
    song_errors = serializers.SongAddSchema().validate(song_data['song_information'])  # ???????????????? ?????????????????? ????????????
    if song_errors:
        return song_errors
    add_song_info.add_song_information(song_data['song_information'])  # ???????????? ???????????? ??????????
    info_about_song['song_id'] = add_song_info.get_song_information(
        song_data['song_information'])  # ???????????????? id ??????????
    if song_data.get('artist_information') is not None:  # ?????????????????? ?????????????? ???????????????????? ???? ??????????????????????
        for artist_info in song_data['artist_information']:
            artist_errors = serializers.ArtistSchema().validate(artist_info)  # ???????????????? ?????????????????? ????????????
            if artist_errors:
                return artist_errors
            add_song_info.add_artist_information(artist_info)  # ???????????? ???????????? ??????????????????????
            info_about_song['artist_id'] = add_song_info.get_artist_information(artist_info)  # ???????????????? id ??????????????????????
            if artist_info.get('album_information') is not None:  # ?????????????????? ?????????????? ???????????????????? ???? ??????????????
                for album_info in artist_info['album_information']:
                    album_errors = serializers.AlbumAddSchema().validate(album_info)  # ???????????????? ?????????????????? ????????????
                    if album_errors:
                        return album_errors
                    add_song_info.add_album_information(album_info)  # ???????????? ???????????? ??????????????
                    info_about_song['album_id'] = add_song_info.get_album_information(album_info)  # ???????????????? id ??????????????
                    ias_errors = serializers.IasSchema().validate(info_about_song)  # ???????????????? ?????????????????? ????????????
                    if ias_errors:
                        return ias_errors
                    add_song_info.info_about_song(info_about_song)  # ???????????? ?????? id ?? ?????????????????????? ??????????????
            else:
                info_about_song['album_id'] = 0
                add_song_info.info_about_song(info_about_song)  # ???????????? ?????? id ?? ?????????????????????? ??????????????, ?????????? album_id
    else:
        info_about_song['artist_id'] = 0
        add_song_info.info_about_song(info_about_song)  # ???????????? ???????????? song_id ?? ?????????????????????? ??????????????


###################################      ????????????????    ###############################################


def delete_song(artist_name, song_name):
    from models import artist as artist_model, song as song_model, album as album_model, info_about_song as ias_model
    song_query = song_model.query.join(ias_model, ias_model.song_id == song_model.song_id) \
        .join(artist_model, artist_model.artist_id == ias_model.artist_id).add_columns(song_model.song_id) \
        .filter(artist_model.artist_name == artist_name.title()).filter(
        song_model.song_name == song_name.title()).first()
    song_id = song_query.song_id
    song_obj = song_model.query.get(song_id)
    return song_obj


###################################      ????????????????????    ###############################################

def update_song(artist_name, song_name, song_data):
    from models import artist as artist_model, song as song_model, info_about_song as ias_model
    errors = serializers.SongUpdateSchema().validate(song_data)
    if errors:
        return errors
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


def update_album(artist_name, album_name, album_data):
    from models import artist as artist_model, album as album_model, info_about_song as ias_model
    errors = serializers.AlbumUpdateSchema().validate(album_data)
    if errors:
        return errors
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
    from models import artist as artist_model
    errors = serializers.ArtistSchema().validate(artist_data)
    if errors:
        return errors
    artist_query = artist_model.query.add_columns(artist_model.artist_id) \
        .filter(artist_model.artist_name == artist_name.title())
    current_artist = artist_model.query.get(artist_query.artist_id)
    current_artist.artist_name = artist_data['artist_name']
    current_artist.artist_info = artist_data['artist_info']
