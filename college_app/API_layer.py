"""
1. get the list of the states (get_states)
    - by default all states (select everything)
2. filter data by enrollment
3. get subset of data as table/df
steps 2 and 3 combined into 1 function (get_subset(state, min_enrollment))
get_flow(source, target, state, min_enrollment)-> df
"""
import pandas as pd

# Constants
DATA_FILE_PATH = "college-scorecard.csv"
STATE_COL = "state"
ADM_RATE_COL = "admission_rate"
MIN_VALUE_ENROLLMENT = 0
# TODO: Add more column constants

class CollegeAPI:
    def __init__(self, filename):
        """Load data from CSV"""
        pass

    def process_data(self):
        """Clean data, bin columns, handle missing values"""
        pass

    def get_states(self):
        """Return list of states for dropdown"""
        pass


    def get_subset(self, state= "all states", min_enrollment=MIN_VALUE_ENROLLMENT):
        """
        return a filtered dataframe
        """


    def get_flow(self, state="All States", left_layer=ADM_RATE_COL,
                 right_layer="completion_rate", min_enrollment=MIN_VALUE_ENROLLMENT):
        """Filter and aggregate data for sankey diagram"""
        pass

def main():
    api = CollegeAPI(DATA_FILE_PATH)


if __name__ == "__main__":
    main()