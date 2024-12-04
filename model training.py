# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load CSV files
file1 = r'C:\Users\fobai\Desktop\Textualpreprocessing/Hurricane_Harvey.csv'  # Replace with the actual path to your first CSV file
file2 = r'C:\Users\fobai\Desktop\Textualpreprocessing/Hurricane_Irma.csv'  # Replace with the actual path to your second CSV file

# Read the data
data1 = pd.read_csv(file1)
data2 = pd.read_csv(file2)

# Merge the two datasets
data = pd.concat([data1, data2], ignore_index=True)

# Check for missing values and drop rows if necessary
data = data.dropna(subset=['processed_data', 'Binary_Class'])  # Ensure these columns have no missing values

# Select features and target
X = data['processed_data']  # Features
y = data['Binary_Class']    # Target (use 'Multiclass' if working on multiclass classification)

# Vectorize the processed_data column
vectorizer = TfidfVectorizer(max_features=5000)  # Adjust max_features based on dataset size
X_transformed = vectorizer.fit_transform(X)

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the model and vectorizer for future use
joblib.dump(model, 'text_classifier_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

# Load and test the saved model (example for inference)
def test_model():
    # Load the saved model and vectorizer
    loaded_model = joblib.load('text_classifier_model.pkl')
    loaded_vectorizer = joblib.load('vectorizer.pkl')

    # Test with a sample text
    sample_text = ["Example processed text for prediction"]
    sample_vectorized = loaded_vectorizer.transform(sample_text)
    prediction = loaded_model.predict(sample_vectorized)
    print("Prediction for the sample text:", prediction)

# Uncomment to test the model after training
test_model()
