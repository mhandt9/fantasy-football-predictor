# fantasy-football-predictor

Here I attempt to predict the in-game points for every player in the popular game La Liga Football Fantasy. Predictions will be uploaded before every gameweek starts to this [website](https://mhandt9.github.io/fantasy-football-predictor/).

## Scraping

I scraped match data from [FBREF](https://fbref.com/en/) and player data specific to the fantasy football game from [FutbolFantasy](https://www.futbolfantasy.com/). The latter was difficult, and required several iterations of trial and error. The final version first scrapes links to the individual player webpages. This is preferrable to an earlier approach that was taking too long as the website was throttling the speed (see complete_scraping.py). However, some manual editing had to be done to fix some broken links. If the csv with the links has been generated: run the scraper, which will create another csv file with the data specific to each player (Name, Position, Team, Points, etc):
```
python scraping_v2.py
```
