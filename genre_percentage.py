import pymysql
import os
import pandas as pd
import matplotlib.pyplot as plt

# database config
db_config = {
    'host': '34.130.173.160',
    'user': 'root',
    'password': 'groupproject',
    'db': 'music_schema'
}

connection = pymysql.connect(**db_config)
try:
    with connection.cursor() as cursor:
        cursor.execute('SET SESSION wait_timeout = 300')
        
        # query search 
        query = """
        SELECT
            YEAR(r.release_date) AS year,
            g.genre_name,
            COUNT(*) AS number_of_songs
        FROM
            bp_track t
        JOIN
            bp_genre g ON t.genre_id = g.genre_id
        JOIN
            bp_release r ON t.release_id = r.release_id
        WHERE
            r.release_date BETWEEN '2000-01-01' AND '2023-12-31'
        GROUP BY
            YEAR(r.release_date), g.genre_name
        ORDER BY
            year, g.genre_name;
        """
        cursor.execute(query)
        results = cursor.fetchall()
       
finally:
    connection.close()

# put in data frame to draw graph
df = pd.DataFrame(results, columns=['Year', 'Genre', 'Number of Songs'])
dir = "C:\\Users\\ICE Terminal Tech\\Desktop\\homework\\big_data\\CSCI620_Group04\\year_genre_percentage"
os.makedirs(dir, exist_ok=True)

# draw graph
for year in df['Year'].unique():
    data = df[df['Year'] == year]
    
    sizes = data['Number of Songs']
    labels = data['Genre']
    
    labels_sizes = list(zip(labels, sizes))
    labels_sizes.sort(key=lambda x: x[1], reverse=True)
    labels, sizes = zip(*labels_sizes)
    
    labels = labels[:10]
    sizes = sizes[:10]
    
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(f'Genre Distribution in {year}(Top 10)')
    
    plt.savefig(os.path.join(dir, f'genre_distribution_{year}.png'))
    plt.close()