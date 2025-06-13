#### 2a. A `scraper.py` module (Second MVP - OOP)

# Now that you've made sure your code works! Let's practice restructuring your solution as a class.

# Code up a `WikipediaScraper` scraper object that allows you to structurally retrieve data from the API.
import requests
import re
import json
import os
import csv
from requests import Session
from bs4 import BeautifulSoup
from utils.config import NAME_REPLACE, RENAME_MAP, COUNTRY_NAMES


class WikipediaScraper:
    # The object should contain at least these six attributes:
    def __init__(
        self,
        base_url: str = "https://country-leaders.onrender.com",
        country_endpoint: str = "/countries",
        leaders_endpoint: str = "/leaders",
        cookies_endpoint: str = "/cookie",
        cookie: object = "",
        countries: list = None,
        broken_url: list = None,
    ):
        self.base_url = base_url
        self.country_endpoint = country_endpoint
        self.leaders_endpoint = leaders_endpoint
        self.cookies_endpoint = cookies_endpoint
        self.leaders_data = {}
        self.cookie = cookie
        self.countries = []
        self.broken_url = []
        self.filename = "leaders"
        self.session = requests.Session()

    # - `refresh_cookie() -> object` returns a new cookie if the cookie has expired
    def refresh_cookie(self) -> object:
        response = self.session.get(f"{self.base_url}/cookie")
        self.cookie = response.cookies.get_dict()
        return self.cookie

    # - `get_countries() -> list` returns a list of the supported countries from the API
    def get_countries(self) -> list:
        countries_response = self.session.get(
            f"{self.base_url}/{self.country_endpoint}", cookies=self.cookie
        )
        if countries_response.status_code == 403:
            countries_response = self.session.get(
                f"{self.base_url}/{self.country_endpoint}",
                cookies=self.refresh_cookie(),
            )
            self.countries = countries_response.json()
        return self.countries

    # - `get_leaders(country: str) -> None` populates the `leader_data` object with the leaders of a country retrieved from the API
    def get_leaders(self, country):
        leaders_response = self.session.get(
            f"{self.base_url}/{self.leaders_endpoint}",
            cookies=self.cookie,
            params={"country": country},
        )
        if leaders_response.status_code == 403:
            leaders_response = self.session.get(
                f"{self.base_url}/{self.leaders_endpoint}",
                cookies=self.refresh_cookie(),
                params={"country": country},
            )
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
            if (
                "other reasons this message may be displayed" in first_paragraph.lower()
                or len(first_paragraph) <= 50
            ):
                self.broken_url.append(wikipedia_eng_url)
            self.leaders_data[country_name].append(
                {
                    "name": name,
                    "wikipedia URL": wikipedia_eng_url,
                    "description": first_paragraph,
                }
            )

    def get_all_leaders(self):
        self.countries = self.get_countries()
        for country in self.countries:
            self.get_leaders(country)

    def replace_eng(self, url, name):
        en_url = re.sub(r"https?://[a-z]{2}\.", "https://en.", url)
        name = re.sub(r"\s", "_", name)
        for old_name, new_name in RENAME_MAP.items():
            en_url = en_url.replace(old_name, new_name)
        if re.search(r"https?://ru", url) or re.search(r"https?://ar", url):
            en_url = "https://en.wikipedia.org/wiki/" + name
        return en_url

    def clean_text(self, p):
        cleaned = re.sub(r"\[.*?\]", "", p)
        cleaned = re.sub(r"\(.*?\)", "", cleaned)
        cleaned = re.sub(r"[ⓘ;)\\]+|\s+", " ", cleaned).strip()
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
    
    def input_filename(self):
        user_input = input("💾 Name your data file (default: leaders): ").strip()
        check_filename = re.search(r'[\\/:*?"<>|]',user_input)
        if not user_input or check_filename:
            self.filename = "leaders"
        else: 
            self.filename = user_input
        return self.filename

    def save_file(self):
        file_extensions = [".json",  ".csv"]
        prompt = input("💾 Save results in a file? (y to confirm): ").strip().lower()
        if prompt == "y":
            file_extension = input("💾  1: .json  2: .csv  or other to cancel: ").strip().lower()
            self.filename = self.input_filename()
            if file_extension == "1" or file_extension in ["json", ".json"]:
                 self.filename += file_extensions[0]
                 print(f"export in {file_extensions[0]} file")
                 self.to_json_file()
                 
            elif file_extension == "2" or file_extension in ["csv", ".csv"]:
                self.filename += file_extensions[1]
                print(f"export in {file_extensions[1]} file")
                self.to_csv_file()
        else:
            print("👋 Skip saving data.")

    # - `to_json_file(filepath: str) -> None` stores the data structure into a JSON file
    def to_json_file(self):
        path = os.path.abspath("")
        access_file = os.path.join(path, "data", self.filename)
        os.makedirs(os.path.dirname(access_file), exist_ok=True)
        with open(access_file, "w") as json_file:
            json.dump(self.leaders_data, json_file, indent=2)
        print(f"✏️ Created {self.filename}")

    def read_file(self):
        path = os.path.abspath("")
        data_dir = os.path.join(path, "data")
        
        if self.filename.endswith(".json") or self.filename.endswith(".csv"):
            access_file = os.path.join(data_dir, self.filename)
        else:
            for file_name in os.listdir(data_dir):
                if file_name.endswith(".json") or file_name.endswith(".csv"):
                    self.filename = file_name  
                    access_file = os.path.join(data_dir, file_name)
                else:
                    print("No .json or .csv file found in 'data/' directory.")
                    return
    
        if self.filename.endswith(".json"):
            with open(access_file, "r") as access_file:
                data = json.load(access_file)
        elif self.filename.endswith(".csv"):
            with open(access_file, mode="r") as access_file:
                data = list(csv.DictReader(access_file))
        return data

    def display(self):
        prompt = input("🖨️ Display results in terminal? (y to confirm): ").strip().lower()
        if prompt == "y":
            print(f"📖 Reading {self.filename}")
            data = self.read_file()
            if not data:
                print("🚫 File not found! Skip display. Exiting.")
                return
            elif isinstance(data, dict):
                for section_key, entries in data.items():
                    for entry in  entries:
                        print(f"\n  {'Country':12}: {section_key}")
                        for key, value in entry.items():
                            print(f"  {key.capitalize():12}: {value}")
            else:
                for line in data :
                    print(f"\n")
                    for key, value in line.items():
                        print(f"  {key.capitalize():12}: {value}")
        else:
            print("👋 Skip display. Exiting.")
            

    def print_broken_urls(self):
        if len(self.broken_url) > 0:
            print("\n⚠️ Cannot access the following Wikipedia URLs:")
            for url in self.broken_url:
                print(url)
                
                
    # an optional CSV export
    
    def to_csv_file(self):

        path = os.path.abspath("")
        access_file = os.path.join(path, "data", self.filename)
        os.makedirs(os.path.dirname(access_file), exist_ok=True)
        
        first_key = list(self.leaders_data.keys())[0]
        fieldnames = ['country'] + list(self.leaders_data[first_key][0].keys())
        
        with open(access_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for country, leaders_list in self.leaders_data.items():
                for leader in leaders_list:
                    row = {'country': country}
                    row.update(leader)
                    writer.writerow(row)
           
    
    # multiprocessing support to speed things up
    
