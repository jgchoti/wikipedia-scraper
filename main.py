from tqdm import tqdm
from utils.scraper import WikipediaScraper


def main() -> None:
    print(f"\n🔍 Getting data...")
    scraper = WikipediaScraper()
    scraper.get_countries()
    for country in tqdm(scraper.countries, desc="Scraping leaders"):
        scraper.get_leaders(country)
    scraper.save_file()
    scraper.display()
    scraper.print_broken_urls()
if __name__ == "__main__":
    main()

