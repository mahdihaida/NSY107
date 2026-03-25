
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('CEAS_08.csv')

# --- Exploratory Data Analysis (EDA) ---
print("--- Data Distribution ---")
dist = df['label'].value_counts(normalize=True) * 100
print(f"Safe Emails (0): {dist.get(0, 0):.2f}%")
print(f"Phishing Emails (1): {dist.get(1, 0):.2f}%")

# Create a visualization for the report
plt.figure(figsize=(8, 6))
sns.countplot(x='label', data=df, palette='viridis')
plt.title('Distribution of Safe vs Phishing Emails')
plt.xlabel('Label (0: Safe, 1: Phishing)')
plt.ylabel('Count')
plt.savefig('eda_distribution.png')
print("EDA chart saved as 'eda_distribution.png'.")

# Preprocessing
X = df['text']
y = df['label']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the TF-IDF vectorizer
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train the SVM model
model = SVC(kernel='linear', probability=True)
model.fit(X_train_tfidf, y_train)

# Make predictions
y_pred = model.predict(X_test_tfidf)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1-Score: {f1}")

# Export the model and vectorizer
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

with open('vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

print("Model and vectorizer exported successfully.")
