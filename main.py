import time
from utils.scraper import WikipediaScraper

def main() -> None:
    print("🔍 Getting data...")
    start = time.time()
    scraper = WikipediaScraper()
    scraper.get_all_leaders()
    filename = "leaders.json"
    scraper.to_json_file(filename)
    scraper.display_json_file(filename)
    time.sleep(1)
    end = time.time()
    scraper.print_broken_urls()
    print(f"\n⌛️ Total runtime is {end - start} seconds")
if __name__ == "__main__":
    main()