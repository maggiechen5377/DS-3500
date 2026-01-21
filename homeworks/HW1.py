import seaborn as sns
import pandas as pd

# Load the Titanic dataset
titanic = sns.load_dataset('titanic')

# Look at the dataset
print(titanic.head())

# Check what sibsp and embarked columns contain
print(titanic[['sibsp', 'embarked']].head(10))
print(titanic['sibsp'].describe())
print(titanic['embarked'].value_counts())

import matplotlib.pyplot as plt

titanic['age'].hist(bins=20)
plt.title('Age Distribution of Titanic Passengers')
plt.xlabel('Age')
plt.ylabel('Number of Passengers')
plt.show()