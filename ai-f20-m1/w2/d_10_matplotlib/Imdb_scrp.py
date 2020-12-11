import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from time import sleep
from random import randint

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    clean = re.sub(clean, '', text)
    clean = clean.split(",")
    return clean


imdb_url = "https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating"
page = requests.get(imdb_url) # requesting the webpage from the internet
soup = BeautifulSoup(page.text, 'html.parser')

bigBoxes = soup.find_all("div",  class_ = "lister-item mode-advanced")
#print(bigBoxes)

Films = {"Name":[], "Description":[], "Duration": [],"Date of Release":[], "Genre":[],"Rating":[],"Director":[],"Actors":[],"Link":[]}

for box in bigBoxes:
    link_string = "https://www.imdb.com" + box.a['href'] 
    print(link_string)
    page = requests.get(link_string) # requesting the webpage from the internet
    soup = BeautifulSoup(page.text, 'html.parser')
    filmBox = soup.find_all('div', class_="heroic-overview")
    #print(filmBox)
    for film in filmBox:
        #print("here")
        name = film.find('h1', class_='')
        if name is None: 
            #print("LONG")
            name = film.find('h1', class_="long")

        description = film.find('div', class_="plot_summary").text
        description = description.replace("                    ","")
        description = description.split("Director:", 1)[0]
        description = description.replace("\n","")
        
        multi_info = film.find('div', class_="subtext").text.replace(" ","").replace("\n","")
        multi_info = multi_info.split('|') #Duration, Genre, Realese Date
        multi_info.pop(0)
        #print("GENERI" + multi_info[1])
        multi_info[1] = multi_info[1].replace(",", ", ")
        multi_info[0] = multi_info[0].replace("h", "h ")

        

        Rating = film.find('span', itemprop="ratingValue").text
        
        Director = " "
        Stars = []
        for a in film.find_all('div', class_="credit_summary_item"):
            if a.find('h4', class_="inline").text == "Director:":
                Director = a.find('a', href=True).text
            if a.find('h4', class_="inline").text == "Directors:":
                Director = remove_html_tags(str(a.find_all('a', href=True)))
            if a.find('h4', class_="inline").text == "Stars:":
                Stars = remove_html_tags(str(a.find_all('a', href=True)))
                Stars[0] = Stars[0].replace("[","")
                Stars.pop(3)
#Films = {"Name":[], "Description":[], "Date of Release":[], "C":[], "Release Date":[],"Rating":[],"Director":[],"Actors":[],"Link":[]}
  
        Films["Name"].append(name.text)
        Films["Description"].append(description)
        Films["Date of Release"] .append(multi_info[2])
        Films["Duration"] .append(multi_info[0])
        Films["Genre"] .append(multi_info[1])
        Films["Rating"].append(Rating)
        Films["Director"].append(Director)
        Films["Actors"].append(Stars)
        Films["Link"].append(link_string)


#print(Films)

dF = pd.DataFrame(Films, index=Films["Name"])
print(dF)