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

def songs_released_over_time(cursor):
    sql = "SELECT * FROM bp_track LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)

    sql = "SELECT SUBSTRING(release_date, 1, 4) AS year, COUNT(*) AS count FROM bp_track GROUP BY SUBSTRING(release_date, 1, 4)"
    cursor.execute(sql)
    result = cursor.fetchall()

    years = []
    counts = []

    for pair in result:
        years.append(int(pair['year']))
        counts.append(pair['count'])
    
    fig = plt.figure(figsize = (10, 5))
    
    plt.bar(years, counts, color ='blue', 
            width = 0.4)
    
    plt.xlabel("Year")
    plt.ylabel("No. of songs released")
    plt.title("Songs released over time")
    plt.show()

def track_duration_over_time(cursor):

    sql = "SELECT SUBSTRING(release_date, 1, 4) AS year, AVG(duration_ms) AS avg_duration FROM bp_track GROUP BY SUBSTRING(release_date, 1, 4);"
    cursor.execute(sql)
    result = cursor.fetchall()

    years = []
    avg_duration_seconds = []

    for pair in result:
        years.append(int(pair['year']))
        avg_duration_seconds.append(int(pair['avg_duration']) / 1000)

    print(avg_duration_seconds)

    fig = plt.figure(figsize = (10, 5))
    
    plt.bar(years, avg_duration_seconds, color ='blue', 
            width = 0.4)
    
    plt.xlabel("Year")
    plt.ylabel("Avg. Song Duration")
    plt.title("Avg. Song Duration Over Time")
    plt.show()


connection = pymysql.connect(host='34.130.173.160',
                             user='root',
                             password='groupproject',
                             database='music_schema',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        songs_released_over_time(cursor)
        track_duration_over_time(cursor)
