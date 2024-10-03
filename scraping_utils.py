from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
import time
from tqdm import tqdm
import csv

class PlayerScraper_All:
    def __init__(self, driver_path, headless=True):
        options = Options()
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("--log-level=1")
        
        if headless:
            options.add_argument("--headless=new")
            
        self.service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=options)
        self.player_data_list = []

    def __accept_cookies(self, driver):
        """Clicks on accept in the cookies pop-up"""
        try:
            # Wait for the cookie banner to be present
            cookies_xpath = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, cookies_xpath)))
            
            # Click the "Accept Cookies" button
            accept_cookies = driver.find_element(By.XPATH, cookies_xpath)
            accept_cookies.click()
            print("Cookies accepted successfully.")
        except TimeoutException:
            print("Cookie banner did not appear.")
        except Exception as e:
            print(f"An error occurred while accepting cookies: {e}")
        
    def open_page(self, url):
        self.driver.get(url)
        self.driver.execute_script("document.body.style.zoom='33%'")
        self.__accept_cookies(self.driver)
        
    def process_players(self, csv_file_name):
        # Open the CSV file in append mode and create a writer object
        with open(csv_file_name, mode='a', newline='', encoding='utf-8') as file:
            fieldnames = ['position', 'team', 'link', 'name'] + [f'Points_GW{i}' for i in range(1, 39)]  # Adjust range if necessary
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write header only if the file is empty or doesn't exist
            if file.tell() == 0:
                writer.writeheader()

            # Find and iterate over all player elements
            player_divs = self.driver.find_elements(By.CLASS_NAME, 'elemento_jugador')

            for i, player in enumerate(tqdm(player_divs, desc="Processing Players", unit="player")):
                try:
                    player_data = {}
                    player_data['position'] = player.get_attribute('data-posicion')
                    player_data['team'] = player.get_attribute('data-equipo')

                    # Click on the player to open their detailed info
                    time.sleep(1.01)
                    player.click()
                    time.sleep(1.01)

                    modal_content = self.driver.find_element(By.CLASS_NAME, 'modal-content')
                    player_data['link'] = self.driver.find_element(By.CLASS_NAME, 'jugador.mt-auto.mb-1.d-flex.mx-auto').get_attribute('href')
                    player_data['name'] = self.driver.find_element(By.CSS_SELECTOR, 'span.d-lg-block:nth-child(2)').text

                    match_divs = self.driver.find_elements(By.CSS_SELECTOR, 'div.row.my-2')

                    for match in match_divs:
                        GW = match.find_element(By.CSS_SELECTOR, 'div.col-2.text-center.p-0').text
                        points = match.find_elements(By.CSS_SELECTOR, 'div.col-3.text-center.p-0')[1].text
                        player_data['Points_GW' + GW] = points

                    # Append the current player's data to the CSV file
                    writer.writerow(player_data)

                    # Return to the main page and wait for the player list to reload
                    self.driver.back()
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'lista_elementos')))
                    player_divs = self.driver.find_elements(By.CLASS_NAME, 'elemento_jugador')

                except TimeoutException:
                    print(f"Timeout occurred while processing player: {player_data.get('name', 'Unknown')}")

                except ElementNotInteractableException:
                    # Retry logic if player interaction fails
                    next_button = self.driver.find_element(By.CSS_SELECTOR, '.next')
                    next_button.click()
                    time.sleep(1.01)
                    self.retry_player(player, csv_file_name)

        
    def retry_player(self, player, csv_file_name):
        player_data = {}
        player_data['position'] = player.get_attribute('data-posicion')
        player_data['team'] = player.get_attribute('data-equipo')

        player.click()
        time.sleep(1.01)

        modal_content = self.driver.find_element(By.CLASS_NAME, 'modal-content')
        player_data['link'] = self.driver.find_element(By.CLASS_NAME, 'jugador.mt-auto.mb-1.d-flex.mx-auto').get_attribute('href')
        player_data['name'] = self.driver.find_element(By.CSS_SELECTOR, 'span.d-lg-block:nth-child(2)').text

        match_divs = self.driver.find_elements(By.CSS_SELECTOR, 'div.row.my-2')

        for match in match_divs:
            GW = match.find_element(By.CSS_SELECTOR, 'div.col-2.text-center.p-0').text
            points = match.find_elements(By.CSS_SELECTOR, 'div.col-3.text-center.p-0')[1].text
            player_data['Points_GW' + GW] = points

        # Open the CSV file in append mode and write this player's data
        with open(csv_file_name, mode='a', newline='', encoding='utf-8') as file:
            fieldnames = ['position', 'team', 'link', 'name'] + [f'Points_GW{i}' for i in range(1, 39)]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(player_data)

        self.driver.back()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'lista_elementos')))

        
    def close(self):
        self.driver.quit()


