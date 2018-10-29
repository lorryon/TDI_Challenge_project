import requests
from bs4 import BeautifulSoup
import csv
import time
import json

imdb_url = []                                                 # Read in the imdb urls generated from crawling douban ratings
with open('douban_top_250_1.csv') as csv_file:
    csv_reader =csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        imdb_url.append(row[3])

imdb_url = imdb_url[1:]

imdb_score_all = []
movie_number = 0

while movie_number < 250:
    time.sleep(15)
    conn = requests.get(imdb_url[movie_number]+'/ratings?ref_=tt_ov_rt')   # Connect to the imdb ratings page that contains detailed rating distribution
    conn.raise_for_status()
    data = conn.content
    if len(data) == 0:
        print('Connection error. Retrying')
        trial += 1
        if trial > 5:
            movie_number += 1
            continue
        else: continue
    soup = BeautifulSoup(data)                                            # Parse the html with BeautifulSoup
    imdb_score = soup.find("div", {"class": "allText"}).text.strip().split()[10]
    imdb_review_count = soup.find("div", {"class": "allText"}).text.strip().split()[0]
    star = [i.text.strip() for i in soup.find_all("div", {"class": "topAligned"})]         # Pull out ratings distribution as a list
    
    time.sleep(15)
    conn = requests.get(imdb_url[movie_number])                  # Connect to imdb movie page that contains basic info about the movie
    conn.raise_for_status()
    data = conn.content
    soup = BeautifulSoup(data)
    info = soup.find("script", {"type": "application/ld+json"}).text   # Basic info in json style, parse with json.loads
    j = json.loads(info)
    movie_name = j["name"]
    movie_genre = j["genre"]
    movie_cast = j.get("actor") #[i["name"] for i in j["actor"]]
    if isinstance(j["director"], list):
        movie_director = [i["name"] for i in j["director"]]
    else: movie_director = j["director"]
    imdb_score_all.append((movie_name, movie_genre, imdb_score, star, imdb_review_count, movie_cast, movie_director))    # Store all info as a list of tuples
    print('Number pulled', movie_number)
    movie_number += 1

with open('douban_top_250_2.csv', 'w', newline='') as csvfile:
    fieldnames = ['Movie Name', 'Movie Genre', 'IMDB Rating', 'IMDB Rating Detail', 'IMDB Review Count', 'Movie Cast', 'Movie Director']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for m in imdb_score_all:
        writer.writerow({'Movie Name': m[0], 'Movie Genre': m[1], 'IMDB Rating': m[2], 'IMDB Rating Detail': m[3], 'IMDB Review Count': m[4], 'Movie Cast': m[5], 'Movie Director': m[6]})
