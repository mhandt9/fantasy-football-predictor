from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
import time
from tqdm import tqdm
import csv
from selenium.webdriver.chrome.options import Options

# run Chrome in headless mode
options = Options()

# disable Blink to disallow images
options.add_argument("--blink-settings=imagesEnabled=false")

# set the options to use Chrome in headless mode (doesnt open browser)
options.add_argument("--headless=new")


# Initialize the WebDriver
service = Service(executable_path='C:/Users/mhand/Selenium/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

# Open the page containing the table of players
driver.get('https://www.futbolfantasy.com/analytics/laliga-fantasy/puntos')

driver.execute_script("document.body.style.zoom='33%'")

def accept_cookies(driver):
        """Clicks on accept in the cookies pop-up"""
        try:
            # Wait for the cookie banner to be present (adjust time if necessary)
            cookies_xpath = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'  # Change this if necessary
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, cookies_xpath)))
            
            # Click the "Accept Cookies" button
            accept_cookies = driver.find_element(By.XPATH, cookies_xpath)
            accept_cookies.click()
            print("Cookies accepted successfully.")
        except TimeoutException:
            print("Cookie banner did not appear.")
        except Exception as e:
            print(f"An error occurred while accepting cookies: {e}")

accept_cookies(driver)

player_data_list = []

player_divs = driver.find_elements(By.CLASS_NAME, 'elemento_jugador')

# Iterate through each player's div
for i, player in enumerate(tqdm(player_divs, desc="Processing Players", unit="player")):
    try:
        player_data = {}

        # Get player link from the main page
        player_data['name'] = player.get_attribute('data-nombre')
        player_data['link'] = 'https://www.futbolfantasy.com/jugadores/'+player_data['name'].replace(' ', '-')

        player_data_list.append(player_data)

        # Wait for the player list to reload before the next iteration
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'lista_elementos')))

        # Re-fetch the player divs (avoid stale elements error)
        player_divs = driver.find_elements(By.CLASS_NAME, 'elemento_jugador')

    except TimeoutException:
        print("Timeout occurred while processing player:", player_data.get('name', 'Unknown'))
        
    except ElementNotInteractableException:

        next_button = driver.find_element(By.CSS_SELECTOR, '.next')
        next_button.click()
        player_data = {}

        # Get player link from the main page
        player_data['name'] = player.get_attribute('data-nombre')
        player_data['link'] = 'https://www.futbolfantasy.com/jugadores/'+player_data['name'].replace(' ', '-')

        player_data_list.append(player_data)

        # Wait for the player list to reload before the next iteration
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'lista_elementos')))

        # Re-fetch the player divs (avoid stale elements error)
        player_divs = driver.find_elements(By.CLASS_NAME, 'elemento_jugador')

# Save data to CSV
csv_file = "player_links.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=player_data_list[0].keys())
    writer.writeheader()
    writer.writerows(player_data_list)

print(f"Links saved to {csv_file}")

driver.quit()