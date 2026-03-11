import pandas as pd
import numpy as np
DATA_FILE_PATH = "boston_311_2026.csv"

# load the dataset
df = pd.read_csv(DATA_FILE_PATH)

# compute the percent of cases that were resolved with "ONTIME"
df_closed = df[df['case_status'] == 'Closed']
ontime_count = (df_closed['on_time'] == 'ONTIME').sum()
total_closed = len(df_closed)
percent = (ontime_count / total_closed) * 100 if total_closed > 0 else 0
print(f'Percentage of resolved cases that were ONTIME: {percent:.2f}%')
