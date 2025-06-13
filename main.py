import time
from utils.scraper import WikipediaScraper


def main() -> None:
    print("🔍 Getting data...")
    start = time.time()
    scraper = WikipediaScraper()
    scraper.get_all_leaders()
    filename = "leaders.json"
    scraper.to_json_file(filename)
    prompt = input("🖨️ Display results in terminal? (y to confirm): ").strip().lower()
    if prompt == "y":
        scraper.display_json_file(filename)
    else:
        print("👋 Skip display. Exiting.")
    end = time.time()
    scraper.print_broken_urls()
    print(f"\n⌛️ Total runtime is {end - start} seconds")


if __name__ == "__main__":
    main()
