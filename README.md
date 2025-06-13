# Wikipedia Scraper

A Python project that fetches information about world leaders via API, scrapes their biographies from Wikipedia, and exports everything into a JSON file. Built as part of my learning at BeCode to deepen experience with APIs, web scraping, and data handling using Python

## 🚀 Current Feature

- Grabs a list of countries and their political leaders via [this API](https://country-leaders.onrender.com/docs).
- Visits each leader’s Wikipedia page to scrape their bio (first paragraph only)
- Cleans the text to remove footnotes and clutter
- Stores everything in a JSON file
- Keeps track of any broken or missing Wikipedia links

## 🛠 Tech

- **Language:** Python 3
- **Libraries:** `requests`, `beautifulsoup4`, `json`, `csv`, `re`

## ⚙️ How to Set It Up

1. Clone this repo:

```bash
git clone https://github.com/jgchoti/wikipedia-scraper.git
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the requirements:

```bash
pip install -r requirements.txt
```

## ▶️ How to Run It

```bash
python main.py
```

This program will save data into `leaders.json` inside the `data/` folder

### 📊 Sample Output in JSON

```json
{
  "USA": [
    {
      "name": "George Washington",
      "Wikipedia Url": "https://en.wikipedia.org/wiki/George_Washington",
      "description": "George Washington was a Founding Father and the first president of the United States, serving from 1789 to 1797. As commander of the Continental Army, Washington led Patriot forces to victory in the American Revolutionary War against the British Empire. He is commonly known as the Father of the Nation for his role in bringing about American independence."
    }
  ]
}
```

---

### 📊 Sample Output in terminal

The program will also ask user if they want to read data and display in their terminal:

```bash

🖨️ Display results in terminal? (y to confirm): y

```

The program will then show output in the terminal

```

📖 Reading leaders.json

  Country     : France
  Name        : François Hollande
  Wikipedia url: https://en.wikipedia.org/wiki/Fran%C3%A7ois_Hollande
  Description : François Gérard Georges Nicolas Hollande is a French politician who served as President of France from 2012 to 2017. Before his presidency, he was First Secretary of the Socialist Party from 1997 to 2008, Mayor of Tulle from 2001 to 2008, as well as President of the General Council of Corrèze from 2008 to 2012. He has also held the 1st constituency of Corrèze seat in the National Assembly three times, first from 1988 to 1993, then from 1997 to 2012, and from 2024 onwards.

```

## ✨ Extra Features (available in the `nice-to-have` branch)

- an optional CSV export
- multiprocessing support to speed things up

## ⚠️ Data Corrections

- Inconsistent or missing leader names from the API were resolved by using their unique IDs and aligning with names from corresponding Wikipedia URLs.

- API-provided Wikipedia links were replaced to the English domain (`en.wikipedia.org`) to ensure consistent in language output.

- Text content was preprocessed before storage, including cleanup of formatting artifacts and removal of citation markers for better readability.

- These modifications were implemented to enhance consistency, and usability.
