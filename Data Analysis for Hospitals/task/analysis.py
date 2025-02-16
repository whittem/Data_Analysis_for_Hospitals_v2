# write your code here
# Dev branch Github
import pandas as pd

pd.set_option('display.max_columns', 8)

general = pd.read_csv(r'./test//general.csv')
prenatal = pd.read_csv(r'./test//prenatal.csv')
sports = pd.read_csv(r'./test//sports.csv')


# function to calculate % share of given diagnosis and hospital
def patient_share(hospital, diagnosis):
    df = df_general
    share_by_hospital = df.groupby("hospital")["diagnosis"].apply(lambda x: (x == diagnosis).mean())
    x = share_by_hospital.loc[hospital].round(3)
    return (x)


# Change column names
prenatal.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'}, inplace=True)
sports.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'}, inplace=True)

# Combine the dataframes
df_general = pd.concat([general, prenatal, sports], ignore_index=True)

# Drop unnamed columns
df_general.drop(columns=['Unnamed: 0'], inplace=True)

# Drop empty rows
df_general.dropna(how='all', inplace=True)

# Correct gender values
df_general['gender'] = df_general['gender'].astype(str).str.lower().str.strip().map(
    lambda x: 'm' if x.startswith('m') else 'f')

# Replace the NaN values in the bmi, diagnosis, blood_test, ecg, ultrasound, mri, xray, children, months columns with zeros
df_general.iloc[:, 6:] = df_general.iloc[:, 6:].fillna(0)

# Hospital with highest number of patients
hosp_max_patients = df_general['hospital'].value_counts().idxmax()

# Share of patients in hosp with issues
stomach_share_general = patient_share('general', 'stomach')
dislocation_share_general = patient_share('sports', 'dislocation')

# Median difference ages general/sports hospitals
age_pivot = df_general.pivot_table(index='hospital', values='age', aggfunc='median')
diff = age_pivot.loc['general'] - age_pivot.loc['sports']

# blood_test_count
highest_hospital = df_general[df_general['blood_test'] == 't']['hospital'].value_counts().idxmax(),
highest_count = df_general[df_general['blood_test'] == 't']['hospital'].value_counts().max()

print(f'The answer to the 1st question is {hosp_max_patients}')
print(f'The answer to the 2nd question is {stomach_share_general}')
print(f'The answer to the 3rd question is {dislocation_share_general}')
print(f'The answer to the 4th question is {float(diff.iloc[0])}')
print(f'The answer to the 5th question is {highest_hospital}, {highest_count} blood tests')
