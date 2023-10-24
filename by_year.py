import matplotlib.pyplot as plt
import numpy as np

def songs_released_over_time(cursor):
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
