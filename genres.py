import matplotlib.pyplot as plt
import numpy as np

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