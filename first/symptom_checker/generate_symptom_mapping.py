import pandas as pd
import os
import json

# Define the path to the dataset
file_path = os.path.join(os.path.dirname(__file__), 'data/dataset.csv')  # Adjust the dataset filename

# Load the dataset
df = pd.read_csv(file_path)

# Extract unique symptoms
symptom_columns = [col for col in df.columns if 'Symptom' in col]
all_symptoms = pd.Series(df[symptom_columns].values.ravel()).dropna().unique()

# Generate mapping
SYMPTOM_MAPPING = {symptom: idx + 1 for idx, symptom in enumerate(all_symptoms)}

# Save mapping to a file
with open('symptom_mapping.json', 'w') as f:
    json.dump(SYMPTOM_MAPPING, f)

print(SYMPTOM_MAPPING)
