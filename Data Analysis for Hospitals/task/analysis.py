# write your code here
# Dev branch Github

import pandas as pd

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
    x = share_by_hospital.loc[hospital].round(3)
    return (x)

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
age_pivot = all_data.pivot_table(index='hospital', values='age', aggfunc='median')
diff = age_pivot.loc['general'] - age_pivot.loc['sports']

# blood_test_count
highest_hospital = all_data[all_data['blood_test'] == 't']['hospital'].value_counts().idxmax(),
highest_count = all_data[all_data['blood_test'] == 't']['hospital'].value_counts().max()

print(f'The answer to the 1st question is {q1}')
print(f'The answer to the 2nd question is {q2}')
print(f'The answer to the 3rd question is {q3}')
print(f'The answer to the 4th question is {float(diff.iloc[0])}')
print(f'The answer to the 5th question is {highest_hospital}, {highest_count} blood tests')
