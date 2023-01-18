import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re
from pprint import pprint
import json
from time import sleep

def get_link(text): 

    """ Достаем ссылки всех вакансий """

    headers = Headers(browser='mozilla',os='win').generate()
    data = requests.get(url=f"https://spb.hh.ru/search/vacancy?text={text}&area=1&area=2&page=1", headers=headers)
    if data.status_code != 200:
        return print('status_code != 200 , (get_link)')    

    soup = BeautifulSoup(data.content,"lxml")
    try:
        page_count = int(soup.find('div', class_='pager').find_all('span',recursive=False)[-1].find('a').find('span').text) #  количество страниц
        print(f"Найдено {page_count} страниц")
    except:
        return   print("Ошибка в page_count ") 
    for page in range(page_count): # проходим по всем странам
        try:     
            data = requests.get(url=f"https://spb.hh.ru/search/vacancy?text={text}&area=1&area=2&page={page}", headers=headers)
            if data.status_code != 200:
                continue 

            soup = BeautifulSoup(data.content,"lxml")
            for link in soup.find_all("a", attrs={"class":"serp-item__title"}): # теги с ссылками 

                yield f"{link.attrs['href'].split('?')[0]}" # возвращяем чистые ссылки вакансий
        except Exception as ex:
            print(f"Ошибка : {ex}")    

        sleep(2)   

def get_vacancies(link):

    ''' Берем даннйе из ссылок '''

    headers = Headers(browser='mozilla',os='win').generate()
    data = requests.get(url=link,headers=headers)
    if data.status_code != 200:
        return print('status_code != 200 , (get_vacancies)') 

    soup = BeautifulSoup(data.content,"lxml")  
    try:
        company_name = soup.find(attrs={"class":"vacancy-company-details"}).text.replace("\xa0"," ") # название компании
    except:
        company_name = "нет данных"
    try:
        salary = soup.find(attrs={"class":"vacancy-title"}).find('span',class_="bloko-header-section-2 bloko-header-section-2_lite").text.replace("\xa0","") # вилка зп
        
    except:
        salary = "нет данных"
    try:
        cities = soup.find(attrs={"class":"vacancy-company-redesigned"}).find("p").text # город
    except:
        cities = "нет данных"

    vacancies = {"название компании":company_name, "вилка зп":salary, "город":cities, "ссылка":link }    
    return vacancies





if __name__ == "__main__":

    data = []
    for i in get_link("python Django Flask"):
        data.append(get_vacancies(i))
        sleep(2)
        with open("data.json","w", encoding="utf=8") as f:
            json.dump(data,f,indent=2,ensure_ascii=False)  