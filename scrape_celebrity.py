import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import json
import time
import random 
from unidecode import unidecode


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Safari/537.36 Edg/99.0.9999.99')
# Utwórz serwis Chrome
chrome_service = ChromeService(ChromeDriverManager().install())
# Utwórz przeglądarkę Chrome z serwisem i opcjami
browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

global parents, kids, partners, siblings

parents = None
kids = None
partners = None
siblings = None

def remove_polish(text):
    text = (
        text.replace("ł", "l")
        .replace("ż", "z")
        .replace("ó", "o")
        .replace("ś", "s")
        .replace("ć", "c")
        .replace("ź", "z")
        .replace("Ł", "L")
        .replace("Ż", "Z")
        .replace("Ó", "O")
        .replace("Ś", "S")
        .replace("Ć", "C")
        .replace("Ź", "z")
        .replace("ę", "e")
        .replace("Ę", "E")
        .replace("ą", "a")
        .replace("Ą", "A")
        .replace("ń", "n")
        .replace("Ń", "N")
    )
    return text


family_list = ['Rodzice', 'Dzieci','Zona', 'Maz', 'Rodzenstwo']

def find_family(family_list, html):

    parents = None
    kids = None
    partners = None
    siblings = None

    for j in html:
        for i in family_list:
            if i in remove_polish(j.find('span', {'class' : 'w8qArf'}).text):
                href = list(map(lambda x: x.get("href"), j.find_all('a', {'class' : 'fl'})))
                names = list(map(lambda x: unidecode(x.text), j.find_all('a', {'class' : 'fl'})))


                if i == 'Rodzice' :
                    parents = [names, href]
                    print('found parents')
                if i == 'Dzieci' :
                    kids = [names, href]
                    print('found kids')
                if i == 'Zona' or i == 'Maz' :
                    partners = [names, href]                    
                    print('found partners')
                if i == 'Rodzenstwo' :
                    siblings = [names, href]
                    print('found siblings')
                
                    
    return [parents, siblings, partners, kids]
            




def save_to_json(celeb_name, names_list, file_name):
    with open(f'{file_name}', 'r') as plik_json:
        dane = json.load(plik_json)

    # Nowe dane do dodania
    nowy_dane = {
        f"{celeb_name}": {
            "rodzice": names_list[0],
            "zony": names_list[2],
            "rodzenstwo": names_list[1],
            "dzieci": names_list[3]
        }
    }

    # Dodanie nowych danych do istniejących danych
    dane.update(nowy_dane)

    # Zapisanie zaktualizowanych danych z powrotem do pliku JSON
    with open(f'{file_name}', 'w') as plik_json:
        json.dump(dane, plik_json, indent=4)

    print("Nowe dane zostały dodane do pliku JSON.")

def find_next_member(file_name):
        with open(f'{file_name}', 'r') as file:
            dane = json.load(file)
            for i in dane: # celebryta, zawsze istnieje 
                for j in dane[i]: # lista rodziny, zawsze istnieje 
                    if dane[i][j] != None:
                        for k in dane[i][j][0]: # konkretne osoby z rodziny
                            if k in dane:
                                continue
                            else:
                                return k, dane[i][j][1][dane[i][j][0].index(k)]
                            
                    else:
                        print("brak członka rodziny")
                        continue

        return None

def soup_page(node_name = None, url = None):
    if not url:
        url_starting_node = node_name.replace(" ", "+")
        url = f'https://www.google.com/search?q={url_starting_node}&num=30'
    else: url  = 'https://www.google.com'+ url
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'search')))
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    return soup


def start_loop(iterations, starting_node, file_name):
    popular_members = 1
    #first node
    soup = soup_page(starting_node)
    items = soup.find_all('div', {'class' : 'rVusze'})
    family = find_family(family_list, items)    
    save_to_json(starting_node, family, file_name)

    #other nodes
    for i in range(iterations):
        time.sleep(random.uniform(30, 50))
        if not find_next_member(file_name):
            print ("No more popular family members. count:", popular_members )
            return
        name, url = find_next_member(file_name)            
        print(url)
        soup = soup_page(url = url)
        items = soup.find_all('div', {'class' : 'rVusze'})
        family = find_family(family_list, items)    
        save_to_json(name, family, file_name)
        popular_members +=1

starting_node = 'Angelina Jolie'
file_name = "angelina_jolie.json"

start_loop(1000, starting_node, file_name)

          