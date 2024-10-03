import argparse
from scraping_utils import PlayerScraper_All

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Scrape player data with Selenium.")
    parser.add_argument('--headless', action='store_true', help="Run the browser in headless mode.")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    driver_path = 'C:/Users/mhand/Selenium/chromedriver-win64/chromedriver.exe'
    url = 'https://www.futbolfantasy.com/analytics/laliga-fantasy/puntos'
    
    # Initialize the scraper with the headless flag
    scraper = PlayerScraper_All(driver_path, headless=args.headless)
    
    # Open the webpage
    scraper.open_page(url)
    
    # Process the player data
    scraper.process_players(csv_file_name='players_data.csv')
    
    # Close the browser
    scraper.close()

if __name__ == "__main__":
    main()