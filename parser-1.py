#IMPORTS
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

#CUSTOM FUNCTIONS
def list_printer(input):
    counter = 1
    for element in input:
        print(f"{counter}. {element}")
        counter += 1

#SETUP
pages_to_parse = 1

headers = {'Accept-Language': 'en-US,en;q=0.8'}
url = 'https://www.rottentomatoes.com/browse/movies_in_theaters/' + '?page=' + str(pages_to_parse)
response = requests.get(url,headers=headers)
parsed_content = BeautifulSoup(response.text, "html.parser")

#DATA COLLECTION (I HATE PRIVACY)
movie_titles = [] #
date_listings = [] #
page_links = [] #
critic_ratings = [] #
audience_ratings = [] #
genres = [] #

print("Getting movie titles...")
for i in parsed_content.select('span.p--small[data-qa="discovery-media-list-item-title"]'):
    movie_titles.append(i.get_text().strip())

print("Getting date listings...")
for i in parsed_content.select('span.smaller[data-qa="discovery-media-list-item-start-date"]'):
    date_listings.append(i.get_text().strip())

print("Getting page links...")
for i in parsed_content.select('a[data-qa="discovery-media-list-item"], a[data-qa="discovery-media-list-item-caption"]'):
    page_links.append('https://www.rottentomatoes.com' + str(i.attrs.get('href')))

print("Getting critic ratings...")
for i in parsed_content.select('rt-text[slot="criticsScore"]'):
    if len(i.get_text().strip()) > 0:
        critic_ratings.append(i.get_text().strip())
    else:
        critic_ratings.append('N/A')

print("Getting audience ratings...")
for i in parsed_content.select('rt-text[slot="audienceScore"]'):
    if len(i.get_text().strip()) > 0:
        audience_ratings.append(i.get_text().strip())
    else:
        audience_ratings.append('N/A')

print("Getting genres...")
for link in page_links:
    temp_response = requests.get(link,headers=headers)
    parsed_page = BeautifulSoup(temp_response.text, "html.parser")
    divs = parsed_page.find_all('div', class_ = 'category-wrap')
    page_genres = []

    for div in divs:
        if div.find('rt-text', string = 'Genre'):
            temp_categories = div.find_all('rt-link')
            for category in temp_categories:
                page_genres.append(category.get_text())
    genres.append(page_genres)


#CONVERTING TO CSV FORM FACTOR
df = pd.DataFrame(
    {
        'movie title'     : movie_titles,
        'date listed'     : date_listings,
        'page link'       : page_links,
        'critic rating'   : critic_ratings,
        'audience rating' : audience_ratings,
        'genres'          : genres
    }
)

df.to_csv('pain.csv', index = False)
print("Complete.")
