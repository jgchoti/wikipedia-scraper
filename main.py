import progressbar
import time
from utils.scraper import WikipediaScraper

def main() -> None:
    print("🔍 Getting data...")
    scraper = WikipediaScraper()
    scraper.get_countries()
    total = len(scraper.countries)
    b = progressbar.ProgressBar(maxval=total)
    b.start()
    start = time.time()
    for i, country in enumerate(scraper.countries):
        scraper.get_leaders(country)
        b.update(i + 1) 
    b.finish()
    time.sleep(1)
    end = time.time()
    filename = "leaders.json"
    scraper.to_json_file(filename)
    prompt = input("🖨️ Display results in terminal? (y to confirm): ").strip().lower()
    if prompt == "y":
        scraper.display_json_file(filename)
    else:
        print("👋 Skip display. Exiting.")
    scraper.print_broken_urls()
    print(f"\n⌛️ Total runtime is {end - start} seconds")
if __name__ == "__main__":
    main()