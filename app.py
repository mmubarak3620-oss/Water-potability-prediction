from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
CORS(app)

# Dataset path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "water_potability.csv")

# Load dataset
df = pd.read_csv(DATA_PATH)

# Input features
features = [
    "ph",
    "Hardness",
    "Solids",
    "Chloramines",
    "Sulfate",
    "Conductivity",
    "Organic_carbon",
    "Trihalomethanes",
    "Turbidity"
]

# Target
target = "Potability"

X = df[features]
y = df[target]

# Fill missing values
imputer = SimpleImputer(strategy="median")
X = imputer.fit_transform(X)

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)

print("Dataset loaded successfully!")
print("Model trained successfully!")


@app.route("/")
def home():
    return "Water Potability Prediction Backend is Running!"


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    print("Received data:", data)

    values = [[
        float(data["ph"]),
        float(data["hardness"]),
        float(data["solids"]),
        float(data["chloramines"]),
        float(data["sulfate"]),
        float(data["conductivity"]),
        float(data["organic_carbon"]),
        float(data["trihalomethanes"]),
        float(data["turbidity"])
    ]]

    # Handle missing values
    values = imputer.transform(values)

    # Prediction
    prediction = int(model.predict(values)[0])

    if prediction == 1:
        result = "Potable (Safe)"
    else:
        result = "Not Potable (Unsafe)"

    return jsonify({
        "prediction": result
    })


if __name__ == "__main__":
    app.run(debug=True)