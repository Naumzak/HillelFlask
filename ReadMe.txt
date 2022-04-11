https://github.com/Naumzak/HillelFlask
Добавлен файл add_song_info.py в котором находятся запросы для добавления полученной информации в базу данных. В самом файле user_data.py находится функция add.song, которая разбирает полученный запрос в формате json и передает информацию в  add_song_info.py. Json для добавления песни должен иметь формат:
{
  "song_info": {
    "song_name": "",
    "song_text": "",
    "year": "",
    "lang": ""
  },
  "artist_info": [
    {
      "artist_name": "",
      "artist_info": "",
      "album_info": [
        {
          "album_name": "",
          "year": "",
          "info": "",
          "track_num": ""
        },
        {
          "album_name": "",
          "year": "",
          "info": "",
          "track_num": ""
        }
      ]
    },
    {
      "artist_name": "",
      "artist_info": ""
    }
  ]
}
Где имена артиста, песни и альбома должны начинаться с заглавных букв. Если какието данные уже есть в базе данных, они будут проигнорированы.

Для удаления песни надо выполнить запрос на адрес песни(/artist/<artist_name>/song/<song_name>) методом DELETE.

Для обновления альбома нужно отправить Json на url альбома(/artist/<artist_name>/album/<album_name>) методом PUT который будет выглядеть следующим образом:
{"album_name": "",
"album_year": "",
"album_info": ""}

Для обновления песни нужно отправить Json на url песни(/artist/<artist_name>/song/<song_name>) методом PUT который будет выглядеть следующим образом:
{"song_name": "",
"song_text": "",
"song_year": "",
"origin_lang": ""}

Для обновления артиста нужно отправить Json на url артиста(/artist/<artist_name>) методом PUT который будет выглядеть следующим образом:
{"artist_name":"",
"artist_info":""}