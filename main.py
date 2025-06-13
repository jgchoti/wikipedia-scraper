from tqdm import tqdm
from utils.scraper import WikipediaScraper


def main() -> None:
    print(f"\n🔍 Getting data...")
    scraper = WikipediaScraper()
    scraper.get_countries()
    for country in tqdm(scraper.countries, desc="Scraping leaders"):
        scraper.get_leaders(country)
    
    user_input = input("Name your data file (default: leaders): ").strip()
    filename = (user_input if user_input else "leaders") + ".json"

    scraper.to_json_file(filename)
    
    prompt = input("🖨️ Display results in terminal? (y to confirm): ").strip().lower()
    if prompt == "y":
        scraper.display_json_file(filename)
    else:
        print("👋 Skip display. Exiting.")
    
    scraper.print_broken_urls()
if __name__ == "__main__":
    main()
