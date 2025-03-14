# write your code here
# Dev branch Github

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 8)

# Function to read csv and amend column names
def handle_frame(name):
    frame = pd.read_csv(name)
    frame.rename(columns={'HOSPITAL': 'hospital', 'Hospital': 'hospital', 'Sex': 'gender', 'Male/female': 'gender'}, inplace=True)
    return frame

# function to calculate % share of given diagnosis and hospital
def patient_share(hospital, diagnosis):
    df = all_data
    share_by_hospital = df.groupby("hospital")["diagnosis"].apply(lambda x: (x == diagnosis).mean())
    return share_by_hospital.loc[hospital].round(3)

# Combine the csv files and call handle_frame function to amend column names
all_data = pd.concat([handle_frame(r'./test//general.csv'), handle_frame(r'./test/prenatal.csv'), handle_frame(r'./test/sports.csv')])

# Drop unnamed columns
all_data.drop(columns=['Unnamed: 0'], inplace=True)

# Drop empty rows
all_data.dropna(how='all', inplace=True)

# Correct gender values
all_data['gender'] = all_data['gender'].astype(str).str.lower().str.strip().map(
    lambda x: 'm' if x.startswith('m') else 'f')

# Replace the NaN values wih zeros
all_data.fillna(0, inplace=True)

# Hospital with highest number of patients
q1 = all_data['hospital'].value_counts().idxmax()

# Share of patients in hosp with issues
q2 = patient_share('general', 'stomach')
q3 = patient_share('sports', 'dislocation')

# Median difference ages general/sports hospitals
q4 = all_data.query("hospital == 'general'")["age"].median() - all_data.query("hospital == 'sports'")["age"].median()
#age_pivot = all_data.pivot_table(index='hospital', values='age', aggfunc='median')
#diff = age_pivot.loc['general'] - age_pivot.loc['sports']

# blood_test_count
highest_hospital = all_data[all_data['blood_test'] == 't']['hospital'].value_counts().idxmax(),
highest_count = all_data[all_data['blood_test'] == 't']['hospital'].value_counts().max()

# Visualise data
# Q1 - What is the most common age of a patient among all hospitals? Plot a histogram and choose one of the following age ranges: 0-15, 15-35, 35-55, 55-70, or 70-80.
bins = [0, 15, 35, 55, 70, 80]
plt.hist(all_data['age'], bins = bins)
plt.title('Age Histogram')
plt.xlabel('Age')
plt.ylabel('Count')
plt.show()

#all_data.to_csv('all_data.csv', index=False)
# Q2 - What is the most common diagnosis among patients in all hospitals? Create a pie chart.
all_data['diagnosis'].value_counts().plot(kind='pie', title='Common Hospital Diagnosis', autopct="%.2f%%")
plt.show()

# Q3
fig, axes = plt.subplots()
sns.violinplot(x='hospital', y='height', data=all_data, ax=axes, palette='coolwarm', hue='hospital', legend=False)
plt.show()


print('The answer to the 1st question: 15-35')
print('The answer to the 2nd question: pregnancy')
print("The answer to the 3rd question: It's because the heights are in different units of measurement ")

