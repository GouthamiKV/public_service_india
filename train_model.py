import pandas as pd
import glob
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Find the complaints CSV file
file = glob.glob("synthetic_indian_citizen_complaints_1000*.csv")[0]

# Load dataset
df = pd.read_csv(file)

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", list(df.columns))


# Input columns
features = [
    "Category",
    "Department",
    "State",
    "City",
    "Status",
    "Pending_Days",
    "Escalated"
]

# Target column
target = "Priority"


# Remove rows with missing values
df = df.dropna(subset=features + [target])


X = df[features]
y = df[target]


# Separate text and number columns
categorical_features = [
    "Category",
    "Department",
    "State",
    "City",
    "Status"
]

numeric_features = [
    "Pending_Days"
]


# Prepare the data
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)


# Create AI model
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000))
    ]
)


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Train the model
model.fit(X_train, y_train)


# Test the model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Training completed!")
print("Model accuracy:", round(accuracy * 100, 2), "%")


# Save trained model
joblib.dump(model, "complaint_priority_model.pkl")

print("Model saved as complaint_priority_model.pkl")