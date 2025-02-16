# write your code here
# Dev branch Github

import pandas as pd

pd.set_option('display.max_columns', 8)

def handle_frame(name):
    frame = pd.read_csv(name)
    frame.rename(columns={'HOSPITAL': 'hospital', 'Hospital': 'hospital', 'Sex': 'gender', 'Male/female': 'gender'}, inplace=True)
    return frame

all_data = pd.concat([handle_frame(r'./test//general.csv'), handle_frame(r'./test/prenatal.csv'), handle_frame(r'./test/sports.csv')])
print(all_data)

#general = pd.read_csv(r'./test//general.csv')
#prenatal = pd.read_csv(r'./test//prenatal.csv')
#sports = pd.read_csv(r'./test//sports.csv')


# function to calculate % share of given diagnosis and hospital
def patient_share(hospital, diagnosis):
    df = all_data
    share_by_hospital = df.groupby("hospital")["diagnosis"].apply(lambda x: (x == diagnosis).mean())
    x = share_by_hospital.loc[hospital].round(3)
    return (x)


# Change column names
#prenatal.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'}, inplace=True)
#sports.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'}, inplace=True)

# Combine the dataframes
#all_data = pd.concat([general, prenatal, sports], ignore_index=True)

# Drop unnamed columns
all_data.drop(columns=['Unnamed: 0'], inplace=True)

# Drop empty rows
all_data.dropna(how='all', inplace=True)

# Correct gender values
all_data['gender'] = all_data['gender'].astype(str).str.lower().str.strip().map(
    lambda x: 'm' if x.startswith('m') else 'f')

# Replace the NaN values in the bmi, diagnosis, blood_test, ecg, ultrasound, mri, xray, children, months columns with zeros
all_data.iloc[:, 6:] = all_data.iloc[:, 6:].fillna(0)

# Hospital with highest number of patients
q1 = all_data['hospital'].value_counts().idxmax()

# Share of patients in hosp with issues
q2 = round(all_data.query("hospital == 'general' and diagnosis == 'stomach'").shape[0] / all_data.query("hospital == 'general'").shape[0], 3)
print(all_data.shape[0])
print(f'This is a test of a better way to code q2. Answer = {q2}')
stomach_share_general = patient_share('general', 'stomach')
dislocation_share_general = patient_share('sports', 'dislocation')

# Median difference ages general/sports hospitals
age_pivot = all_data.pivot_table(index='hospital', values='age', aggfunc='median')
diff = age_pivot.loc['general'] - age_pivot.loc['sports']

# blood_test_count
highest_hospital = all_data[all_data['blood_test'] == 't']['hospital'].value_counts().idxmax(),
highest_count = all_data[all_data['blood_test'] == 't']['hospital'].value_counts().max()

print(f'The answer to the 1st question is {q1}')
print(f'The answer to the 2nd question is {stomach_share_general}')
print(f'The answer to the 3rd question is {dislocation_share_general}')
print(f'The answer to the 4th question is {float(diff.iloc[0])}')
print(f'The answer to the 5th question is {highest_hospital}, {highest_count} blood tests')
