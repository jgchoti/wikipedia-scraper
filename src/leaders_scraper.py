import requests
import re
import json
import os
import time
from requests import Session
from bs4 import BeautifulSoup

NAME_REPLACE = {
    "Q57553" : "Mohammed VI of Morocco",
    "Q69103" : "Hassan II of Morocco",
    "Q193874" : "Mohammed V of Morocco",
    "Q334782" : "Abu Abdallah al-Qaim"
}

COUNTRY_NAMES = {
    'fr' : "France",
    'be': "Belgium" ,
    'ma' : "Morocco",
    'us': "USA",
    'ru': "Russia"
}

def replace_eng(url,name):
   en_url = re.sub(r'https?://[a-z]{2}\.', "https://en.", url)
   name = re.sub(r"\s", "_", name)
   name = re.sub('(homme_d%27%C3%89tat)', "(statesman)", name)
   if re.search(r"https?://ru", url) or re.search(r"https?://ar", url):
       en_url = "https://en.wikipedia.org/wiki/" + name
       
   return en_url

def clean_text(p):
    cleaned = re.sub(r'\[.*?\]', "", p)
    cleaned = re.sub(r'\[[^\]]*\d+[^\]]*\]', "", cleaned)
    cleaned = re.sub(r'\(.*?\)', "", cleaned)
    cleaned = re.sub(r'[ⓘ;)\\]+|\s+', " ", cleaned).strip() 
    return cleaned

def get_first_paragraph(wikipedia_url):
    session = requests.Session()
    response = session.get(wikipedia_url)
    soup = BeautifulSoup(response.text, "html.parser")
    div_tag = soup.find("div", class_="mw-content-ltr")
    if div_tag:
        p_tags = div_tag.find_all("p")
        for p in p_tags:
            if p.get("class") is None:
                text = p.get_text()
                clean_paragraph = clean_text(text)
                if clean_paragraph and clean_paragraph.strip().lower() != "defunct":
                    return clean_paragraph
    return "⚠️ no description found"
              
def get_fresh_cookies(root_url):
    session = requests.Session()
    response = session.get(f"{root_url}/cookie")
    return response.cookies.get_dict()

def get_leaders():
    print("🔍 Getting data...")
    # define the urls
    start = time.time()
    root_url ="https://country-leaders.onrender.com"
    countries_url = "countries"
    leaders_url = "leaders"
    # get the countries
    session = requests.Session()
    cookies = get_fresh_cookies(root_url)
    countries = session.get(f"{root_url}/{countries_url}", cookies=cookies).json()
    # loop over them and save their leaders in a dictionary
    leaders = {}
    for country in countries:
        #  get leaders data
        leaders_response = session.get(f"{root_url}/{leaders_url}", cookies=cookies,params={"country":country})
        if leaders_response.status_code == 403:
            leaders_response = session.get(f"{root_url}/{leaders_url}", cookies=get_fresh_cookies(root_url, session),params={"country":country})
        leaders_list = leaders_response.json()
        #  replace country to  more readable
        country_name = COUNTRY_NAMES[country]
        leaders[country_name] = []
        for leader in leaders_list:
            if country == "ma":
                name = NAME_REPLACE[leader["id"]]
            else:
                name = leader["first_name"] + " " + leader["last_name"]

            wikipedia_url = leader["wikipedia_url"]
            wikipedia_eng_url = replace_eng(wikipedia_url, name)
            first_paragraph = get_first_paragraph(wikipedia_eng_url)
            if first_paragraph == 'Other reasons this message may be displayed:':
                wikipedia_eng_url = wikipedia_url
                first_paragraph = get_first_paragraph(wikipedia_url)
            leaders[country_name].append({
            "name": name,
            "Wikipedia Url" : wikipedia_eng_url,
            "description": first_paragraph
        })
    time.sleep(1)
    end = time.time()
    print(f"Total runtime is {end - start} seconds")
    return leaders

def save(leaders_per_country, filename):
   path = os.path.abspath("")
   access_file = os.path.join(path, "data", filename)
   os.makedirs(os.path.dirname(access_file), exist_ok=True)
   with open(access_file, 'w') as json_file:
       json.dump(leaders_per_country, json_file, indent=2)

def read(filename):
    path = os.path.abspath("")
    access_file = os.path.join(path, "data", filename)
    with open(access_file, 'r') as json_file:
	    data = json.load(json_file)
    print(f"✏️ Created {filename}")
    return data

def display(filename):
    print(f"📖 Reading {filename}")
    data = read(filename)
    for section_key, entries in data.items():  
        print(f"\n📍 {section_key}")
        for idx, entry in enumerate(entries, 1):
            print(f"\n  Entry {idx}")
            for field_key, field_value in entry.items():
                print(f"  {field_key.capitalize():12}: {field_value}")

        
filename = "leaders.json"
leaders_per_country = get_leaders()
save(leaders_per_country, filename)
display(filename)

