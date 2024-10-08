import requests
from bs4 import BeautifulSoup
import re
import csv
from tqdm import tqdm
import pandas as pd

data = []
# bad_links = []
# other_errors = []

with open('data/player_links.csv', newline='') as csvfile:
        
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')

    next(reader)

    for i, link in enumerate(tqdm(reader, total=752)):

        try:
            
            player_data = {}

            response = requests.get(link[1], timeout=10)
            response.raise_for_status()


            soup = BeautifulSoup(response.content, 'html.parser')

            XPlay = soup.find('div', class_='pct').get_text()
            name = soup.select('span.d-none.d-lg-inline-block')[0].get_text()
            team_name = soup.select_one('div.img-underphoto a').get_text().strip()

            player_data['Name'] = name
            player_data['TeamName'] = team_name
            player_data['XPlay'] = XPlay


            point_boxes = soup.select('span.racha-box.columna_puntos.point.mx-auto.laliga-fantasy')

            points = []

            for box in point_boxes:
                text = box.get_text()
                p = re.findall(r'-?\d+', text)
                points.extend(p)

            table = soup.find('table', class_='tablestats')
            rows = table.find_all('tr', class_='plegado plegable')

            for i, row in enumerate(rows):
                GW = row.find('td', class_=re.compile(r'bold')).get_text()
                # print(f'Gameweek {GW}: {points[i]}')
                player_data['Points_GW'+GW] = points[i]

            data.append(player_data)

        except requests.exceptions.RequestException as e:
            # print(f"Error fetching {link[1]}: {e}")
            # bad_links.append(link)
            pass
        except Exception as e:
            # print(f"An error occurred with {link[1]}: {e}")
            # other_errors.append(link)
            pass

df = pd.DataFrame(data)
df.to_csv('data/players.csv', index=False)