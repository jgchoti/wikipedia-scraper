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

## ✨ Extra Features (available in the `feature` branch)

- an optional CSV export
- multiprocessing support to speed things up
