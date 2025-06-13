import multiprocessing
from tqdm import tqdm
from utils.scraper import WikipediaScraper


def get_data(country):
    local_scraper = WikipediaScraper()
    leaders = local_scraper.get_leaders(country)
    return {
        "country": leaders[0],
        "leaders": leaders[1],
        "broken_urls": local_scraper.broken_url 
    }

def main() -> None:
    print(f"\n🔍 Getting data...")
    scraper = WikipediaScraper()
    countries = scraper.get_countries()
    all_data= []
    with multiprocessing.Pool() as pool:
        for result in tqdm(pool.imap_unordered(get_data, countries), total=len(countries), desc="Fetching leaders data"):
            all_data.append(result)
            
    for element in all_data:
        scraper.leaders_data[element["country"]] = element["leaders"]
        scraper.broken_url.extend(element["broken_urls"])

    scraper.save_file()
    scraper.display()
    scraper.print_broken_urls()
if __name__ == "__main__":
    main()

