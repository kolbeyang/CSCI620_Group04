"""
File used to perform analysis based on genres

genres_per_artist : creates a histogram showing how many genres
    artist tend to create music under
genres_audio_features : finds the average audio features
    for the top five genres in the database
"""

import matplotlib.pyplot as plt
import numpy as np
import pymysql.cursors

def genres_per_artist(cursor):
    sql = """
        SELECT bp_artist_track.artist_id AS artist_id, COUNT(DISTINCT bp_track.genre_id) AS genre_count, COUNT(bp_track.track_id) AS track_count
        FROM bp_artist_track INNER JOIN bp_track ON bp_artist_track.track_id=bp_track.track_id
        GROUP BY bp_artist_track.artist_id;
    """
    cursor.execute(sql)
    result = cursor.fetchall()

    genres_per_artist = [pair['genre_count'] for pair in result]

    fig = plt.figure(figsize = (10, 5))
    
    plt.hist(genres_per_artist, 24)
    
    plt.xlabel("Genres per artist")
    plt.ylabel("Number of artists")
    plt.title("Genres per artist")
    plt.show()

def genres_audio_features(cursor):
    # sql = """
    #     SELECT bp_genre.genre_name FROM bp_track JOIN bp_genre ON bp_track.genre_id=bp_genre.genre_id GROUP BY bp_genre.genre_id ORDER BY COUNT(*) DESC LIMIT 15
    # """
    sql = """
        SELECT 
            bp_genre.genre_name AS genre,
            AVG(audio_features.acousticness) AS avg_acousticness, 
            AVG(audio_features.danceability) AS avg_danceability,
            AVG(audio_features.energy) AS avg_energy,
            AVG(audio_features.instrumentalness) AS avg_instrumentalness,
            AVG(audio_features.liveness) AS avg_liveness
        FROM bp_track 
        INNER JOIN bp_genre ON bp_track.genre_id=bp_genre.genre_id
        INNER JOIN audio_features ON bp_track.isrc=audio_features.isrc 
        GROUP BY bp_track.genre_id
        ORDER BY COUNT(bp_track.track_id) ASC
        LIMIT 5
    """

    cursor.execute(sql)
    result = cursor.fetchall()

    genres = [entry['genre'] for entry in result]
    accousticness_values = [entry['avg_acousticness'] for entry in result]
    danceability_values = [entry['avg_danceability'] for entry in result]
    energy_values = [entry['avg_energy'] for entry in result]
    instrumentalness_values = [entry['avg_instrumentalness'] for entry in result]
    liveness_values = [entry['avg_liveness'] for entry in result]
    
    
    X_axis = np.arange(len(genres)) 
    
    plt.bar(X_axis - 0.3, accousticness_values, 0.1, label = 'Acousticness') 
    plt.bar(X_axis - 0.2, danceability_values, 0.1, label = 'Danceability') 
    plt.bar(X_axis - 0.1, energy_values, 0.1, label = 'Energy') 
    plt.bar(X_axis + 0, instrumentalness_values, 0.1, label = 'Instrumentalness') 
    plt.bar(X_axis + 0.1, liveness_values, 0.1, label = 'Liveness') 
    
    plt.xticks(X_axis, genres) 
    plt.xlabel("Groups") 
    plt.ylabel("Quantifier (0 - 1)") 
    plt.title("Acoustic Features by Genre") 
    plt.legend() 
    plt.show() 

# Connect to the database
connection = pymysql.connect(host='34.130.173.160',
                             user='root',
                             password='groupproject',
                             database='music_schema',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # genres_per_artist(cursor)
        genres_audio_features(cursor)
