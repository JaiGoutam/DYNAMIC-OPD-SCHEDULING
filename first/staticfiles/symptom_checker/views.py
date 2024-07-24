# symptom_checker/views.py
import joblib
import os
import json
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse

# Load the saved model and encoder
model_path = os.path.join(os.path.dirname(__file__), 'symptom_checker_model.pkl')
model, encoder = joblib.load(model_path)

# Load the symptom mapping
with open(os.path.join(os.path.dirname(__file__), 'symptom_mapping.json'), 'r') as f:
    SYMPTOM_MAPPING = json.load(f)

def symptom_checker_home(request):
    return render(request, 'symptom_checker/home.html')

def symptom_checker_form(request):
    return render(request, 'symptom_checker/form.html')

def symptom_checker_api(request):
    if request.method == 'POST':
        symptoms = [
            request.POST.get('symptom1'),
            request.POST.get('symptom2'),
            request.POST.get('symptom3'),
            request.POST.get('symptom4'),
            request.POST.get('symptom5'),
            request.POST.get('symptom6'),
            request.POST.get('symptom7')
        ]
        
        # Map symptoms to their corresponding values
        symptoms_mapped = [SYMPTOM_MAPPING.get(symptom, 0) for symptom in symptoms]
        
        prediction = predict_disease(symptoms_mapped)
        return JsonResponse({'prediction': prediction})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def predict_disease(symptoms):
    try:
        # Initialize symptom data with all zeros
        symptom_data = {f'Symptom_{i+1}': 0 for i in range(len(SYMPTOM_MAPPING))}
        
        # Set the values for symptoms present in the input
        for symptom_value in symptoms:
            symptom_column = f'Symptom_{symptom_value}'
            if symptom_column in symptom_data:
                symptom_data[symptom_column] = 1
        
        # Create DataFrame and ensure column order
        input_df = pd.DataFrame([symptom_data])
        input_df = input_df.reindex(sorted(input_df.columns), axis=1)

        # One-hot encode the input data
        input_vector = encoder.transform(input_df)

        # Predict using the model
        prediction = model.predict(input_vector)
        return prediction[0]
    except Exception as e:
        print(f"Error in prediction: {e}")
        return "undefined"
