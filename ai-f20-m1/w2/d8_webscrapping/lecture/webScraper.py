import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get("https://weather.com/weather/tenday/l/69bedc6a5b6e977993fb3e5344e3c06d8bc36a1fb6754c3ddfb5310a3c6d6c87")
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id ='WxuDailyCard-main-a43097e1-49d7-4df7-9d1a-334b29628263')
#print(results.prettify())
weather_el =  results.find_all('div', class_='DailyForecast--DisclosureList--350ZO')



def today_weather(data_input):
    for data in data_input:
        date_of_today = data.find('span', class_="DailyContent--daypartDate--3MM0J")
        temp_of_today = data.find('span', class_="DailyContent--temp--_8DL5")
        description_text = data.find('p', class_="DailyContent--narrative--3AcXd")
        print(date_of_today.text)
        print(temp_of_today.text)

def get_tenDays(data_input):
    fin_dic = {"Day":[],"TempMax": [], "TempMin": [], "Text": []}
    for data in data_input:
        for i in range(1,10,1):
            string = "detailIndex{}".format(i)
            temp_data = data.find_all('div', id=string)
            #print(temp_data)
            
            for value in temp_data:
                temp_day = value.find('h2', class_= "DetailsSummary--daypartName--1Mebr")
                temp_temp_max = value.find('span', class_="DetailsSummary--highTempValue--3x6cL")
                temp_temp_min = value.find('span', class_="DetailsSummary--lowTempValue--1DlJK")
                temp_description = value.find('span', class_="DetailsSummary--extendedData--aaFeV")
                fin_dic["Day"].append(temp_day.text)
                fin_dic["TempMax"].append(temp_temp_max.text)
                fin_dic["TempMin"].append(temp_temp_min.text)
                fin_dic["Text"].append(temp_description.text)
                #result.append({'maxTemp': temp_temp_max,'minTemp': temp_temp_min,'Text': temp_description }, ignore_index = True)
                print(temp_day.text)
                print(temp_temp_max.text)
                print(temp_temp_min.text)
                print(temp_description.text)
    result = pd.DataFrame(fin_dic)

    print(result)


today_weather(weather_el)

get_tenDays(weather_el)
#for we in weather_el:
#   print(we, end='\n'*2)

#for we in weather_el:
#    title_elem = we.find('h1', class_='LocationPageTitle--PageHeader--3bC6K DailyForecast--CardHeader--1IoG-')
#    title_elem2 = title_elem.find('span', class_='LocationPageTitle--PresentationName--Injxu')
#    print(title_elem2.text)
