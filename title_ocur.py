import pymysql
from collections import Counter
import os
import matplotlib.pyplot as plt

# database config
db_config = {
    'host': '34.130.173.160',
    'user': 'root',
    'password': 'groupproject',
    'db': 'music_schema'
}

# words we dont want to count with
bad_words = set([
    'the', 'of', 'and', 'a', 'in', 'to', 'it', 'is', 'you', 'that', 'was',
    'he', 'for', 'on', 'are', 'with', 'as', 'his', 'they', 'at', 'be', 'this',
    'have', 'from', 'or', 'one', 'had', 'by', 'word', 'but', 'not', 'what',
    'all', 'were', 'we', 'when', 'your', 'can', 'said', 'there', 'use', 'an',
    'each', 'which', 'she', 'do', 'how', 'their', 'if', 'will', 'up', 'about',
    'out', 'many', 'then', 'them', 'these', 'so', 'some', 'her', 'would',
    'make', 'like', 'him', 'into', 'time', 'has', 'look', 'two', 'more', 'write',
    'go', 'see', 'number', 'no', 'way', 'could', 'people', 'my', 'than', 'first',
    'water', 'been', 'call', 'who', 'oil', 'its', 'now', 'find', 'long', 'down',
    'day', 'did', 'get', 'come', 'made', 'may', 'part','feat.' , '&','(feat.'
])

# connect to database and do query search
connection = pymysql.connect(**db_config)

query = """
SELECT t.title, g.genre_name
FROM bp_track t
JOIN bp_genre g ON t.genre_id = g.genre_id;
"""
try:
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
finally:
    connection.close()

word_count = {}
song_count = Counter()
common_word = Counter()
total_word = Counter()

# Top 15 words appear in genres
for title, genre_name in results:
    song_count[genre_name] += 1
    
    words = title.lower().split()
    words = [word for word in words if word not in bad_words]
    
    if genre_name not in word_count:
        word_count[genre_name] = Counter()
    word_count[genre_name].update(words)

# edit with your path to store
charts_dir = "C:\\Users\\ICE Terminal Tech\\Desktop\\homework\\big_data\\CSCI620_Group04\\title_ocur"
charts_dir_pie = "C:\\Users\\ICE Terminal Tech\\Desktop\\homework\\big_data\\CSCI620_Group04\\top20_common"
os.makedirs(charts_dir_pie, exist_ok=True)
os.makedirs(charts_dir, exist_ok=True)

# draw graph
for genre, counter in word_count.items():   

    words = [word for word, count in counter.most_common(15)]
    counts = [count for word, count in counter.most_common(15)]
    
    plt.figure(figsize=(10, 8))
    plt.bar(words, counts, color='blue')
    plt.title(f"Top 15 words in {genre} music titles")
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    
    plt.xticks(rotation=45, ha="right")

    for i in range(len(counts)):
        plt.text(i, counts[i] + 0.05 * max(counts), counts[i], ha = 'center')
    
    path = os.path.join(charts_dir, f"{genre.replace('/', '_')}_chart.png")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()  

# Top 20 words that appear in all genres
for genre, words in word_count.items():
    for word, count in words.items():
        common_word[word] += 1
        total_word[word] += count

number_of_genres = 32
words_in_all_genres = [word for word, count in common_word.items() if count == number_of_genres]
top_20_words = sorted(words_in_all_genres, key=lambda word: total_word[word], reverse=True)[:20]

words = [word for word in top_20_words]
counts = [total_word[word] for word in top_20_words]

# plot pie chart to store
plt.figure(figsize=(10, 8))
plt.pie(counts, labels=words, autopct='%1.1f%%', startangle=140)
plt.axis('equal') 
plt.title('Top 20 Words in All 32 Genres')
path = os.path.join(charts_dir_pie, f"top20_chart.png")
plt.savefig(path)
plt.close()  

# for test 
# print("Top 20 words that appear in all genres:")
# for word in top_20_words:
#     print(f"{word}: {total_word_counts[word]}")
# for genre, counter in word_count.items():
#     print(f"music type: {genre}")
#     print(f"number of songs: {song_count[genre]}")
#     for word, count in counter.most_common(15):  
#         print(f"{word}: {count}")
#     print("\n")  