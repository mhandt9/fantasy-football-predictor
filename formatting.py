import pandas as pd
import numpy as np

class Formatting:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe.copy()

    def __target_and_previous(self):
        """Prepares the target column as the player performance in points as well as the last three performances."""
        # Initialize the new columns
        self.dataframe['Target'] = np.nan
        self.dataframe['Points_Tmin1'] = np.nan
        self.dataframe['Points_Tmin2'] = np.nan
        self.dataframe['Points_Tmin3'] = np.nan

        for wk in self.dataframe['Wk'].unique():
            wk = int(wk)

            # Check if Points_GW{wk} column exists and assign 'Target'
            target_column = f'Points_GW{wk}'

            if target_column in self.dataframe.columns:
                # Assign values to the 'Target' column for all rows where Wk == wk
                self.dataframe.loc[self.dataframe['Wk'] == wk, 'Target'] = self.dataframe.loc[self.dataframe['Wk'] == wk, target_column].values

            # else:
            #     self.dataframe = self.dataframe[self.dataframe['Wk'] != wk]

            # Assign Tmin values based on prior GWs
            if wk - 1 > 0 and f'Points_GW{wk-1}' in self.dataframe.columns:
                self.dataframe.loc[self.dataframe['Wk'] == wk, 'Points_Tmin1'] = self.dataframe.loc[self.dataframe['Wk'] == wk, f'Points_GW{wk-1}'].values
            if wk - 2 > 0 and f'Points_GW{wk-2}' in self.dataframe.columns:
                self.dataframe.loc[self.dataframe['Wk'] == wk, 'Points_Tmin2'] = self.dataframe.loc[self.dataframe['Wk'] == wk, f'Points_GW{wk-2}'].values
            if wk - 3 > 0 and f'Points_GW{wk-3}' in self.dataframe.columns:
                self.dataframe.loc[self.dataframe['Wk'] == wk, 'Points_Tmin3'] = self.dataframe.loc[self.dataframe['Wk'] == wk, f'Points_GW{wk-3}'].values

        # Drop all 'Points_GW' columns
        gw_columns = [col for col in self.dataframe.columns if col.startswith('Points_GW')]
        self.dataframe.drop(gw_columns, axis=1, inplace=True)

    def __home_dummy(self):
        """Sets column Home to 1 if the player belongs to the team playing at home, else 0."""

        self.dataframe['Home?'] = np.where(self.dataframe['Home_id'] == self.dataframe['TeamId'], 1, 0)

        self.dataframe['Opponent'] = np.where(self.dataframe['Home?'] == 1, self.dataframe['Away'], self.dataframe['Home'])
        self.dataframe['Opponent_id'] = np.where(self.dataframe['Home?'] == 1, self.dataframe['Away_id'], self.dataframe['Home_id'])
        self.dataframe.drop(['Away_id', 'Home_id', 'Away', 'Home'], axis=1, inplace=True)

    def __reorder(self):
        """Sets final ordering of columns."""

        final_order = ['Wk', 'Name', 'TeamName', 'Home?', 'TeamId', 'Opponent', 'Opponent_id', 'Points_Tmin1', 'Points_Tmin2', 'Points_Tmin3', 'Target']
        self.dataframe = self.dataframe[final_order]


    def preprocess(self):
        """Returns dataframe upon applying all preprocessing steps."""

        self.__target_and_previous()

        self.__home_dummy()

        self.__reorder()

        return self.dataframe
