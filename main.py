import pymysql.cursors
import by_year
import genres

username = input("PLease enter the username: ")
password = input("Please enter the password: ")

# Connect to the database
connection = pymysql.connect(host='34.130.173.160',
                             user=username,
                             password=password,
                             database='music_schema',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # by_year.songs_released_over_time(cursor)
        # by_year.track_duration_over_time(cursor)
        # genres.genres_per_artist(cursor)
        genres.genres_audio_features(cursor)
