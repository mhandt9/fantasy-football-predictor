# fantasy-football-predictor

Here I attempt to predict the in-game points for every player in the popular game La Liga Football Fantasy. Predictions will be uploaded before every gameweek starts to this [website](https://mhandt9.github.io/fantasy-football-predictor/).

## Scraping

I scraped match data from [FBREF](https://fbref.com/en/) and player data specific to the fantasy football game from [FutbolFantasy](https://www.futbolfantasy.com/). The latter was difficult, and required several iterations of trial and error. To run the scraper, which will create a csv file with the data specific to each player (Name, Position, Team, Points, etc), run: 
```
python scraping_v2.py
```
