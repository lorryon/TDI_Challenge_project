import requests
import random
import string
from bs4 import BeautifulSoup
import csv
import time

lurl = 'https://movie.douban.com/top250'      # url for douban top 250 movie listing
page_num  = 0
movie = []
page_url = lurl
while True:
    time.sleep(15)
    conn = requests.get(page_url, cookies={"Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))})  # cookies with random generated bid needed to connect to douban server
    data = conn.content
    soup = BeautifulSoup(data)                       # Parse the html with BeautifulSoup
    movielist = soup.select('.grid_view li')
    for m in movielist:                              # Pull out rank, movie title and their douban url
        rank = m.select('em')[0].text
        raw_title = m('span')[1].contents[0]
        title = raw_title[2:]
        movie_url = m.a.get('href')
        movie.append((rank, title, movie_url))

    if soup.select('.next a'):                      # Find the link for next page
        asoup = soup.select('.next a')[0]['href']
        page_url = lurl + asoup
        page_num += 1
    else:
        print('stop')
        break
 
 with open('douban_top_250.csv', 'w', newline='') as csvfile:                # Write the info into csv
    fieldnames = ['Ranking', 'Title', 'Douban URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for m in movie:
        writer.writerow({'Ranking': m[0], 'Title': m[1], 'Douban URL': m[2]})

douban_url = []                                             # Read in the list of douban urls and use them to access douban review ratings
with open('douban_top_250.csv') as csv_file:
    csv_reader =csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        douban_url.append(row[2])

douban_url = douban_url[1:]
douban_score_all = []
movie_number = 0

while movie_number < 250:
    trial = 1
    time.sleep(15)
    conn = requests.get(douban_url[movie_number], cookies={"Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))})
    data = conn.content
    if len(data) == 0:
        print('Connection error. Retrying')
        trial += 1
        if trial > 5:
            movie_number += 1
            continue
        else: continue
    soup = BeautifulSoup(data)                                    # Parse the html with BeautifulSoup
    douban_rating = soup.strong.text                                          # Douban ratings for this movie (in scale of 10)
    douban_review_count = soup.find("span", {"property": "v:votes"}).text     # Number of reviews for this movie
    star = []                                                                 # Ratings distribution (in 1 to 5 stars)
    for str in soup.find_all(attrs={"class": "rating_per"}):
        star.append(str.text)
    parsed_url = soup.find_all("a", {"target": "_blank", "rel": "nofollow"})  # The corresponding imdb url
    if len(parsed_url) > 1:
        imdb_url = parsed_url[1].get('href')
    else: imdb_url = parsed_url[0].get('href')
    douban_score_all.append((douban_score, star, douban_review_count, imdb_url))
    print('Number pulled', movie_number)
    movie_number += 1
 
 with open('douban_top_250_1.csv', 'w', newline='') as csvfile:                  # Write into csv file 
    fieldnames = ['Douban Rating', 'Rating Detail', 'Review Count', 'IMDB URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for m in douban_score_all:
        writer.writerow({'Douban Rating': m[0], 'Rating Detail': m[1], 'Review Count': m[2], 'IMDB URL': m[3]})
