import time
from utils.scraper import WikipediaScraper


def main() -> None:
    print("🔍 Getting data...")
    start = time.time()
    scraper = WikipediaScraper()
    scraper.get_all_leaders()
    filename = "leaders.json"
    scraper.to_json_file(filename)
    scraper.close()
    end = time.time()
    prompt = input("🖨️ Display results in terminal? (y to confirm): ").strip().lower()
    if prompt == "y":
        scraper.display_json_file(filename)
    else:
        print("👋 Skip display. Exiting.")

    scraper.print_broken_urls()
    print(f"\n⌛️ Total runtime is {round(end - start, 2)} seconds")

if __name__ == "__main__":
    main()
