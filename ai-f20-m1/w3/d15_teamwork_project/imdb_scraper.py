import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import matplotlib.pyplot as plt
page = requests.get("https://www.imdb.com/list/ls066676482/?st_dt=&mode=detail&page=1&sort=user_rating,desc&genres=Action&title_type=movie&ref_=ttls_ref_yr")
soup = BeautifulSoup(page.content, "html.parser")

mgm_film_data = soup.find_all('div', class_ = "lister list detail sub-list")

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    clean = re.sub(clean, '', text)
    #clean = clean.split(",")
    return clean

def get_titles(input_data):
    titles = []
    years = []
    for data in input_data:
        film = data.find_all('div', class_='lister-item-content')
        for info in film:
            title_info = info.find('h3', class_="lister-item-header")
            title = title_info.find('a').text
            year = title_info.find('span', class_="lister-item-year text-muted unbold").text
            year = year.replace("(", "")
            year = year.replace(")", "")
            year = int(year)
            titles.append(title)
            years.append(year)
    return(titles, years)

def get_duration(input_data):
    durations = []
    for data in input_data:
        film = data.find_all('div', class_='lister-item-content')
        for info in film:
            title_info = info.find('p', class_="text-muted text-small")
            duration = str(title_info.find('span', class_='runtime'))
            duration = remove_html_tags(duration)
            duration = duration.replace(" min","")
            if duration != 'None': duration = int(duration)
            else: duration = float("NaN")
            durations.append(duration)
    return durations

def get_description(input_data):
    descriptions = []
    for data in input_data:
        film = data.find_all('div', class_='lister-item-content')
        for info in film:
            description = info.find('p', class_='').text
            description = re.sub("^\s+|\s+$", "", description, flags=re.UNICODE)
            description = re.sub(r'\.\.\..*',"",description)
            if "Add a Plot" in description:
                description = "No description Present in the database"
            descriptions.append(description)

    return(descriptions)

def get_rating(input_data):
    ratings = []
    for data in input_data:
        film = data.find_all('div', class_='lister-item-content')
        for info in film:
            rating = info.find('span', class_="ipl-rating-star__rating").text
            rating = float(rating)
            ratings.append(rating)
    return ratings

def get_directors(input_data):
    directors = []
    for data in input_data:
        film = data.find_all('p', class_='text-muted text-small')[1:]
        for i in film:
            directors_names = i.find('a')
            directors_names = remove_html_tags(str(directors_names))
            if directors_names != 'None':
                directors.append(directors_names)
    return directors   
        #directors.append(director)
    #return director

def create_dataFrame(input_data):
    data = {"Movie Title": get_titles(input_data)[0],
            "Years": get_titles(input_data)[1],
            "Duration": get_duration(input_data),
            "Rating": get_rating(input_data),
            "Description": get_description(input_data),
            "Directors": get_directors(input_data)}
    df = pd.DataFrame(data)
    return df

def print_graph1(mgm_data):
    print("Mean Value Rating of the MGM 44 action Movie: " + str(round(mgm_data['Rating'].mean(), 2)))
    print("Mean Duration of MGM 44 Action Movie: " + str(round(mgm_data['Duration'].mean(), 0)))
    print("Mean Year Production of MGM 44 Action Movie: " + str(round(mgm_data['Years'].mean(), 0)))
    print(mgm_data.Directors.mode())
    plt.figure(figsize=(12.5,10))
    ax1 = plt.scatter(mgm_data['Years'],mgm_data['Movie Title'],s=150, color='gold')
    ax1 = plt.grid(b=True)
    ax1 = plt.rc('grid', linestyle="-", color='black')
    ax1 = plt.xlabel("Years", fontsize=15)
    ax1 = plt.ylabel("Title Films", fontsize=15)
    ax1 = plt.title("Films Over Time", fontsize=20)
    plt.show()

def print_graph2(mgm_data):
    plt.figure(figsize=(10,7))
    plt.bar(mgm_data['Years'],mgm_data['Rating'], color='Gold',label="Variation of Ratings over time")
    plt.title("Variation of Ratings over Films")
    plt.xlabel("Years")
    plt.ylabel("Ratings Value")
    mean = mgm_data['Rating'].mean()
    line = plt.axhline(mean)
    plt.legend(loc='upper right')
    plt.show()

#print(get_directors(mgm_film_data))
#get_description(mgm_film_data)
mgm_data = create_dataFrame(mgm_film_data)
print_graph1(mgm_data)
print_graph2(mgm_data)
#mgm_data.sort_value('Duration')
#h = plt.hist(mgm_data['Duration'],mgm_data['Rating'])
#plt.show()