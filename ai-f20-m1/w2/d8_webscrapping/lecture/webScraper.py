import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

page = requests.get("https://weather.com/weather/tenday/l/69bedc6a5b6e977993fb3e5344e3c06d8bc36a1fb6754c3ddfb5310a3c6d6c87")
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id ='WxuDailyCard-main-a43097e1-49d7-4df7-9d1a-334b29628263')

#Get the element from the main box
weather_el =  results.find_all('div', class_='DailyForecast--DisclosureList--350ZO')

#Function to convert F° to C°      
def convert_temp(string):
    string = string.replace('°','')
    temp_c = (int(string) - 32) * (5/9)
    string = str(int(temp_c)) + "°"
    return string

def plot_temp(dataF):
    fig = plt.gca()
    #fig.suptitle('Variation of Temperature Max and Min')
    dataF['Day'] = dat
    dataF.plot(kind = "line",x= "Day", y="TempMax",color='red', ax=fig)
    dataF.plot(kind = "line",x= "Day", y="TempMin", ax=fig)
    plt.show()

#Create the Data Frame and Store on it the information
def get_tenDays(data_input):
    fin_dic = {"Day":[],"Date": [],"TempMax": [], "TempMin": [], "Condition": [], "ItemName": []}
    for data in data_input:
        temp_day = data.find('span', class_="DailyContent--daypartDate--3MM0J")
        temp_temp_max = data.find('span', class_="DailyContent--temp--_8DL5")
        temp_temp_min = data.find('span', class_="DailyContent--temp--_8DL5" ) #Cannot Get the minimum temperature
        temp_description = data.find('p', class_="DailyContent--narrative--3AcXd")
        fin_dic["Day"].append(temp_day.text)
        fin_dic["Date"].append("") #TO BE COMPLETED
        fin_dic["TempMax"].append(convert_temp(temp_temp_max.text))
        fin_dic["TempMin"].append(convert_temp(temp_temp_min.text))
        fin_dic["Condition"].append(temp_description.text)
        fin_dic["ItemName"].append("DailyContent--daypartDate--3MM0J")
    
    for data in data_input:
        for i in range(1,11,1):
            string = "detailIndex{}".format(i)
            temp_data = data.find_all('div', id=string)
            #print(temp_data)
            for value in temp_data:
                temp_day = value.find('h2', class_= "DetailsSummary--daypartName--1Mebr")
                temp_temp_max = value.find('span', class_="DetailsSummary--highTempValue--3x6cL")
                temp_temp_min = value.find('span', class_="DetailsSummary--lowTempValue--1DlJK")
                temp_description = value.find('span', class_="DetailsSummary--extendedData--aaFeV")
                fin_dic["Day"].append(temp_day.text)
                fin_dic["Date"].append("") # TO BE COMPLETED
                fin_dic["TempMax"].append(convert_temp(temp_temp_max.text))
                fin_dic["TempMin"].append(convert_temp(temp_temp_min.text))
                fin_dic["Condition"].append(temp_description.text)
                fin_dic["ItemName"].append(string)
                

    result = pd.DataFrame(fin_dic, index= fin_dic["Day"])
    return result

print(get_tenDays(weather_el))
#plot_temp(get_tenDays(weather_el))


