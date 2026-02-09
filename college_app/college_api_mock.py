"""
API Layer - MOCK
This code does not actually do
any of the API functions, you will
need to implement functionality here
 if you'd like to see the app working
correctly.
"""
from logging import critical

import pandas as pd

DATA_FILE_PATH = "college-scorecard.csv"
STATE_COL = "state"
ADM_RATE_COL = "admission_rate"
MEDIAN_EARNINGS_COL = "median_earnings_10yr"
COMPLETION_RATE_COL = "completion_rate"
ENROLLMENT_COL = "enrollment"
LEFT_LAYER_COL_NAME = ADM_RATE_COL
RIGHT_LAYER_COL_NAMES = [MEDIAN_EARNINGS_COL, COMPLETION_RATE_COL]
CRIT_COLS = [STATE_COL, LEFT_LAYER_COL_NAME]
IMPUT_COLS = RIGHT_LAYER_COL_NAMES
BIN_SPECS = {
        ADM_RATE_COL: {
            'bins': [0, 0.30, 0.70, 1.0],
            'labels': ['Highly Selective', 'Selective', 'Open Access'],
            },
        COMPLETION_RATE_COL: {
            'bins': [-1, 0, 0.40, 0.60, 1.0],
            'labels': ['Unspecified', 'Low', 'Medium', 'High']
            },
        MEDIAN_EARNINGS_COL: {
            'bins': [-1, 0, 32000, 43000, 56000, 150000],
            'labels': ['Unspecified', 'Low (less than 32k)', 'Medium-Low (32-43k)',
                       'Medium-High (43-56k)', 'High (56-150k)']
        }
    }

class CollegeAPI:
    def __init__(self, filename):
        """ Loads the data into the dataframe.
        filename: path to CSV file.
        """
        self.college_data = pd.read_csv(DATA_FILE_PATH)

    def process_data(self, critical_columns=CRIT_COLS, imputable_columns=IMPUT_COLS, bin_specs=BIN_SPECS):
        """
        Will perform data processing actions based on args.
        critical_columns: (list of str) columns that cannot be NaN. Will get dropped.
        imputable_columns: (list of str) columns that get assigned a -1 if absent.
        bin_specs: dict where key is column names, values can be:
            - int: number of quantiles (automatic binning)
            - dict: {'bins': [...], 'labels': [...]} for manual binning
        :return: None. Mutates the dataframe in the object.
        """
        #TODO: process the data

    def get_states(self):
        """Returns sorted list of unique states for dropdown, with All States on top"""
        states = self.college_data[STATE_COL].unique().tolist()
        states.sort()
        return ["All States"]

    def get_subset(self, state="All States",
                 min_enrollment = 0):
        """Returns the filtered subset of data."""
        return self.college_data

    def get_flow(self, state="All States",
                 left_layer=LEFT_LAYER_COL_NAME,
                 right_layer=RIGHT_LAYER_COL_NAMES[0],
                 min_enrollment = 0):
        """
        Reports count by two variables, left and right.
        Includes "All States" in the counts.
        Filters by minimum enrollment.
        Returns the summary as a dataframe.
        """
        # old code!
        return pd.DataFrame({
            LEFT_LAYER_COL_NAME: ["A", "B", "A"],
            RIGHT_LAYER_COL_NAMES[0]: ["C", "D", "D"],
            RIGHT_LAYER_COL_NAMES[1]: ["C", "D", "C"],
            "count": [40, 2, 2]
        })

def main():
    api = CollegeAPI(DATA_FILE_PATH)
    api.process_data()
    print(api.college_data)
    print(api.get_states())
    print(api.get_flow())

if __name__ == "__main__":
    main()