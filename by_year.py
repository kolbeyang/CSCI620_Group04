"""
File used to perform analysis based on year

songs_released_over_time : shows the number of songs released
    per year in the database

track_duration_over_time : shows the average duration of songs
    released per year
"""

import matplotlib.pyplot as plt
import numpy as np
import pymysql.cursors

"""
Shows the number of songs released per year in the database
"""
def songs_released_over_time(cursor):
    sql = """SELECT YEAR(bp_release.release_date) AS year, COUNT(*) AS count 
        FROM bp_track INNER JOIN bp_release ON bp_track.release_id=bp_release.release_id
        GROUP BY YEAR(bp_release.release_date)"""
    cursor.execute(sql)
    result = cursor.fetchall()

    # Separate data into years and counts lists
    years = []
    counts = []
    for pair in result:
        years.append(int(pair['year']))
        counts.append(pair['count'])
    
    fig = plt.figure(figsize = (10, 5))
    
    # Create bar graph
    plt.bar(years, counts, color ='blue', 
            width = 0.4)
    
    # Adding labels
    plt.xlabel("Year")
    plt.ylabel("No. of songs released")
    plt.title("Songs released over time")
    plt.show()

"""
Shows the average duration of songs released per year
"""
def track_duration_over_time(cursor):

    sql = """SELECT YEAR(bp_release.release_date) AS year, AVG(bp_track.duration_ms) AS avg_duration 
        FROM bp_track INNER JOIN bp_release ON bp_track.release_id=bp_release.release_id
        GROUP BY YEAR(bp_release.release_date)"""
    cursor.execute(sql)
    result = cursor.fetchall()

    # Separate data into years and avg_duration_seconds
    years = []
    avg_duration_seconds = []
    for pair in result:
        years.append(int(pair['year']))
        avg_duration_seconds.append(int(pair['avg_duration']) / 1000)

    fig = plt.figure(figsize = (10, 5))
    
    # Create bar graph
    plt.bar(years, avg_duration_seconds, color ='blue', 
            width = 0.4)
    
    # Adding labels
    plt.xlabel("Year")
    plt.ylabel("Avg. Song Duration")
    plt.title("Avg. Song Duration Over Time")
    plt.show()

# Connect to DB
connection = pymysql.connect(host='34.130.173.160',
                             user='root',
                             password='groupproject',
                             database='music_schema',
                             cursorclass=pymysql.cursors.DictCursor)

# Call the above functions with DB connection
with connection:
    with connection.cursor() as cursor:
        songs_released_over_time(cursor)
        track_duration_over_time(cursor)
