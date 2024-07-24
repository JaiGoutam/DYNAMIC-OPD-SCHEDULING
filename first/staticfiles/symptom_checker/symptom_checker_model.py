# symptom_checker/symptom_checker_model.py


import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
import os

# Load your dataset
def load_dataset():
    file_path = os.path.join(os.path.dirname(__file__), 'data/dataset.csv')  # Update the path
    data = pd.read_csv(file_path)
    X = data.drop(columns=['Disease'])  # Updated to match the dataset
    y = data['Disease']  # Updated to match the dataset
    return X, y

# One-hot encode the symptom data
def one_hot_encode(X):
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X)
    return X_encoded, encoder

# Train and save the model
def train_and_save_model():
    X, y = load_dataset()
    X_encoded, encoder = one_hot_encode(X)
    model = DecisionTreeClassifier()
    model.fit(X_encoded, y)
    joblib.dump((model, encoder), os.path.join(os.path.dirname(__file__), 'symptom_checker_model.pkl'))  # Save both the model and the encoder

if __name__ == "__main__":
    train_and_save_model()
