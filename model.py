import pandas as pd
import json
from formatting import Formatting # from formatting.py
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

MWS_PLAYED = 11

players = pd.read_csv('data/players.csv')
matches = pd.read_csv('data/matches.csv') # from fbref.com

# Rename some teams to more consistent names
players = players.replace('Athletic', 'Athletic Club')
players = players.replace('Atlético', 'Atlético Madrid')
players = players.replace('Celta', 'Celta Vigo')
players = players.replace('Rayo', 'Rayo Vallecano')


# Get and apply Team ids
with open('club_ids.json', 'r') as fp:
        club_mapping = json.load(fp)

players['TeamId'] = players['TeamName'].map(club_mapping)


# Merge and concat to get a dataframe where each player in every match has a row
home_matches_by_player = pd.merge(left=matches, right=players, left_on='Home_id', right_on='TeamId', how='left')
away_matches_by_player = pd.merge(left=matches, right=players, left_on='Away_id', right_on='TeamId', how='left')
matches_by_player = pd.concat([home_matches_by_player, away_matches_by_player]).drop(['Time', 'Date', 'xG', 'xG.1', 'Day', 'Score', 'XPlay'], axis=1)

formatter = Formatting(matches_by_player)

df1 = formatter.preprocess()


# Model can't run with missing values. I arbitrarily assign -5 to represent that the player did not play in that match
df1_clean = df1.fillna(value=-5).drop(['Opponent', 'TeamName'], axis=1)
df1_clean = df1_clean[df1_clean['Wk'] > 3]


# Label Encoding of the Players for example: 
enc = LabelEncoder()
df1_clean['Name'] = enc.fit_transform(df1_clean['Name'])


# Filter to matchweeks already played to train the model
X_train = df1_clean[df1_clean['Wk'] < MWS_PLAYED].drop(['Target', 'Wk'], axis=1)
y = df1_clean[df1_clean['Wk'] < MWS_PLAYED]['Target']


# Next matchweek as X_test
X_test = df1_clean[df1_clean['Wk'] == MWS_PLAYED].drop(['Target', 'Wk'], axis=1)


# Training and predicting
regr = RandomForestRegressor(n_estimators=200, max_depth=None, random_state=0)
regr.fit(X_train, y)
preds = regr.predict(X_test)
prediction = pd.DataFrame({'Name':enc.inverse_transform(X_test['Name']), 'Prediction':preds})


# Print feature importances
print(f'Feature importances: {regr.feature_importances_}')


# Arbitrarily decide that predictions below -2 are predicting the player not to play
prediction['Prediction'] = prediction['Prediction'].apply(lambda x: round(x) if x > -2 else 'NOT PLAYING').astype(str)


# Sort descending and save as CSV
def sort_preds(df):
    df['helper_col'] = pd.to_numeric(df['Prediction'], errors='coerce')

    df_sorted = df.sort_values(by='helper_col', ascending=False, na_position='last')

    return df_sorted.drop('helper_col', axis=1)

prediction = sort_preds(prediction)
prediction.to_csv('GW'+str(MWS_PLAYED)+'_pred.csv', index=False)