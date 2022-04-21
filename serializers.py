from marshmallow import Schema, fields, validate
import constants


class SongUpdateSchema(Schema):
    song_name = fields.Str(required=True, validate=validate.Length(min=1))
    song_text = fields.Str(required=False, validate=validate.Length(min=2))
    song_year = fields.Int(required=False, validate=validate.Range(min=1900, max=2500))
    origin_lang = fields.Str(required=False, validate=validate.OneOf(constants.LANG_CODES))


class AlbumUpdateSchema(Schema):
    album_name = fields.Str(required=True, validate=validate.Length(min=1))
    album_year = fields.Int(required=False, validate=validate.Range(min=1900, max=2500))
    album_info = fields.Str(required=False, validate=validate.Length(min=1))


class ArtistSchema(Schema):
    artist_name = fields.Str(required=True, validate=validate.Length(min=1))
    artist_info = fields.Str(required=False, validate=validate.Length(min=1))


class SongAddSchema(Schema):
    song_name = fields.Str(required=True, validate=validate.Length(min=1))
    song_text = fields.Str(required=True, validate=validate.Length(min=2))
    song_year = fields.Int(required=False, validate=validate.Range(min=1900, max=2500))
    origin_lang = fields.Str(required=True, validate=validate.OneOf(constants.LANG_CODES))


class AlbumAddSchema(Schema):
    album_name = fields.Str(required=True, validate=validate.Length(min=1))
    album_year = fields.Int(required=True, validate=validate.Range(min=1900, max=2500))
    album_info = fields.Str(required=False, validate=validate.Length(min=1))


class IasSchema(Schema):
    artist_id = fields.Int(required=True)
    song_id = fields.Int(required=True)
    album_id = fields.Int(required=True)
