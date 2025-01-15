import tkinter as tk
from tkinter import ttk
import pickle
import pandas as pd
from datetime import datetime

# Load the saved model
with open('car_price_predictor_model.sav', 'rb') as file:
    model = pickle.load(file)

df = pd.read_csv('car data.csv')  
car_names = df['Car_Name'].unique().tolist()

# Define feature preprocessing
def preprocess_input(price, kms, fuel_type, selling_type, transmission, owner, year):
    # Calculate Age from the manufacturing year
    current_year = datetime.now().year
    age = current_year - year

    # Create a dictionary of all features expected by the model in the correct order
    data = {
        'Year': [year],  # Include 'Year' feature
        'Present_Price': [price],
        'Driven_kms': [kms],
        'Owner': [owner],
        'Age': [age],  # Include the calculated 'Age' feature
        'Fuel_Type_CNG': [1 if fuel_type == 'CNG' else 0],
        'Fuel_Type_Diesel': [1 if fuel_type == 'Diesel' else 0],
        'Fuel_Type_Petrol': [1 if fuel_type == 'Petrol' else 0],
        'Selling_type_Dealer': [1 if selling_type == 'Dealer' else 0],
        'Selling_type_Individual': [1 if selling_type == 'Individual' else 0],
        'Transmission_Automatic': [1 if transmission == 'Automatic' else 0],
        'Transmission_Manual': [1 if transmission == 'Manual' else 0]
    }

    # Convert the dictionary into a DataFrame
    df = pd.DataFrame(data)

    # Ensure the features are in the same order as they were in training
    correct_order = [
        'Year', 'Present_Price', 'Driven_kms', 'Owner', 'Age', 'Fuel_Type_CNG', 
        'Fuel_Type_Diesel', 'Fuel_Type_Petrol', 'Selling_type_Dealer', 'Selling_type_Individual', 
        'Transmission_Automatic', 'Transmission_Manual'
    ]
    
    # Reorder columns to match the correct order
    df = df[correct_order]

    return df

# GUI implementation
root = tk.Tk()
root.title("Car Price Predictor")

# Title label
title_label = tk.Label(root, text="Car Price Predictor", font=("Helvetica", 16))
title_label.grid(row=0, column=1, pady=10)

# Input fields
labels = [
    "Present Price (in lakhs):", "Driven (Kms):", "Fuel Type (Petrol/Diesel/CNG):",
    "Selling Type (Dealer/Individual):", "Transmission (Manual/Automatic):",
    "Number of Owners:", "Manufacturing Year:"
]
entries = []

for i, label in enumerate(labels):
    tk.Label(root, text=label).grid(row=i + 1, column=0, padx=10, pady=5)
    if i == 2:
        entry = ttk.Combobox(root, values=["Petrol", "Diesel", "CNG"])
    elif i == 3:
        entry = ttk.Combobox(root, values=["Dealer", "Individual"])
    elif i == 4:
        entry = ttk.Combobox(root, values=["Manual", "Automatic"])
    else:
        entry = tk.Entry(root)
    entry.grid(row=i + 1, column=1, padx=10, pady=5)
    entries.append(entry)

# Predict button and result label
def predict_price():
    try:
        # Collect input values
        price = float(entries[0].get())
        kms = int(entries[1].get())
        fuel_type = entries[2].get()
        selling_type = entries[3].get()
        transmission = entries[4].get()
        owner = int(entries[5].get())
        year = int(entries[6].get())

        # Preprocess inputs
        input_data = preprocess_input(price, kms, fuel_type, selling_type, transmission, owner, year)

        # Make prediction
        prediction = model.predict(input_data)
        result_label.config(text=f"Predicted Price: {prediction[0]:.2f} Lakhs")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

predict_button = tk.Button(root, text="Predict Price", command=predict_price)
predict_button.grid(row=len(labels) + 1, column=1, pady=20)

result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.grid(row=len(labels) + 2, column=1, pady=10)

# Run the application
root.mainloop()
