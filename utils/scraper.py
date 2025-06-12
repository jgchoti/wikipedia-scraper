#### 2a. A `scraper.py` module (Second MVP - OOP)

# Now that you've made sure your code works! Let's practice restructuring your solution as a class.

# Code up a `WikipediaScraper` scraper object that allows you to structurally retrieve data from the API.
import requests
import re
import json
import os
from requests import Session
from bs4 import BeautifulSoup
from utils.config import NAME_REPLACE, RENAME_MAP,COUNTRY_NAMES

class WikipediaScraper:
# The object should contain at least these six attributes:
    def __init__(self, base_url: str = "https://country-leaders.onrender.com", country_endpoint: str = "/countries", leaders_endpoint: str = "/leaders"
                 , cookies_endpoint: str = "/cookie", leaders_data: dict = None, cookie: object = "", countries: list = None, broken_url: list = None):
        self.base_url = base_url
        self.country_endpoint = country_endpoint 
        self.leaders_endpoint = leaders_endpoint
        self.cookies_endpoint = cookies_endpoint
        self.leaders_data = {}
        self.cookie = cookie
        self.countries = []
        self.broken_url = []
        self.session = requests.Session()
        
# - `refresh_cookie() -> object` returns a new cookie if the cookie has expired
    def refresh_cookie(self) -> object:
        response = self.session.get(f"{self.base_url}/cookie")
        self.cookie =  response.cookies.get_dict()
        return self.cookie 

# - `get_countries() -> list` returns a list of the supported countries from the API
    def get_countries(self) -> list:
        countries_response = self.session.get(f"{self.base_url}/{self.country_endpoint}", cookies=self.cookie)
        if countries_response.status_code == 403:
            countries_response = self.session.get(f"{self.base_url}/{self.country_endpoint}", cookies=self.refresh_cookie())
            self.countries = countries_response.json()
        return self.countries
        
# - `get_leaders(country: str) -> None` populates the `leader_data` object with the leaders of a country retrieved from the API
    def get_leaders(self, country):
        leaders_response = self.session.get(f"{self.base_url}/{self.leaders_endpoint}", cookies=self.cookie ,params={"country":country})
        if leaders_response.status_code == 403:
            leaders_response = self.session.get(f"{self.base_url}/{self.leaders_endpoint}", cookies=self.refresh_cookie(),params={"country":country})        
        leaders_list = leaders_response.json()
        #  replace country to  more readable
        country_name = COUNTRY_NAMES[country]
        self.leaders_data[country_name] = []
        for leader in leaders_list:
            if country == "ma":
                name = NAME_REPLACE[leader["id"]]
            else:
                name = leader["first_name"] + " " + leader["last_name"]

            wikipedia_url = leader["wikipedia_url"]
            wikipedia_eng_url = self.replace_eng(wikipedia_url, name)
            first_paragraph = self.get_first_paragraph(wikipedia_eng_url)
            if "other reasons this message may be displayed" in first_paragraph.lower() or len(first_paragraph) <= 50:
                self.broken_url.append(wikipedia_eng_url )
            self.leaders_data[country_name].append({
            "name": name,
            "Wikipedia URL" : wikipedia_eng_url,
            "description": first_paragraph
        })
    
    def get_all_leaders(self):
        self.countries = self.get_countries()
        for country in self.countries:
            self.get_leaders(country)
        
    def replace_eng(self,url,name):
        en_url = re.sub(r'https?://[a-z]{2}\.', "https://en.", url)
        name = re.sub(r"\s", "_", name)
        for old_name, new_name in RENAME_MAP.items():
            en_url = en_url.replace(old_name, new_name)
        if re.search(r"https?://ru", url) or re.search(r"https?://ar", url):
            en_url = "https://en.wikipedia.org/wiki/" + name
        return en_url
    
    def clean_text(self, p):
        cleaned = re.sub(r'\[.*?\]', "", p)
        cleaned = re.sub(r'\[[^\]]*\d+[^\]]*\]', "", cleaned)
        cleaned = re.sub(r'\(.*?\)', "", cleaned)
        cleaned = re.sub(r'[ⓘ;)\\]+|\s+', " ", cleaned).strip() 
        return cleaned
    
# - `get_first_paragraph(wikipedia_url: str) -> str` returns the first paragraph (defined by the HTML tag `<p>`) with details about the leader
    def get_first_paragraph(self, wikipedia_url: str) -> str:
        response = self.session.get(wikipedia_url)
        if response.status_code != 200:
            self.broken_url.append(wikipedia_url)
        soup = BeautifulSoup(response.text, "html.parser")
        div_tag = soup.find("div", class_="mw-content-ltr")
        if div_tag:
            p_tags = div_tag.find_all("p")
            for p in p_tags:
                if p.get("class") is None:
                     if p.find_parent(class_="sidebar-list"):
                        continue
                     text = p.get_text()
                     clean_paragraph = self.clean_text(text)
                     if clean_paragraph and clean_paragraph.strip().lower() != "defunct":
                        return clean_paragraph
        return "⚠️ no description found"
    
# - `to_json_file(filepath: str) -> None` stores the data structure into a JSON file
    def to_json_file(self, filename:str):
        path = os.path.abspath("")
        access_file = os.path.join(path, "data", filename)
        os.makedirs(os.path.dirname(access_file), exist_ok=True)
        with open(access_file, 'w') as json_file:
            json.dump(self.leaders_data, json_file, indent=2)
        print(f"✏️ Created {filename}")

    def read_json_file(self,filename):
        path = os.path.abspath("")
        access_file = os.path.join(path, "data", filename)
        with open(access_file, 'r') as json_file:
            data = json.load(json_file)
        
        return data
    
    def display_json_file(self,filename):
        print(f"📖 Reading {filename}")
        data = self.read_json_file(filename)
        for section_key, entries in data.items():  
            print(f"\n📍 {section_key}")
            for idx, entry in enumerate(entries, 1):
                print(f"\n  Entry {idx}")
                for key, value in entry.items():
                    print(f"  {key.capitalize():12}: {value}")
                    
    def print_broken_urls(self):
        if len(self.broken_url) > 0:
            print("\n⚠️ Cannot access the following Wikipedia URLs:")
            for url in self.broken_url:
                print(url)
                
                
    # an optional CSV export
    
    # multiprocessing support to speed things up
    