import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load existing data
df = pd.read_csv('/home/orasniper/oracle-chatbot/data/oracle_errors.csv')

# Simulate new data (replace with actual feedback loop)
new_errors = pd.DataFrame([{
    'code': 'ORA-12345',
    'description': 'New error',
    'cause': 'Test cause',
    'solution': 'Test solution'
}])
df = pd.concat([df, new_errors], ignore_index=True)

# Feature engineering (simplified example)
X = df['description']
y = df['code']

# Train a classifier (for intent recognition)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
classifier = RandomForestClassifier()
classifier.fit(X_train, y_train)

# Save the updated model
joblib.dump(classifier, '//home/orasniper/oracle-chatbot/models/error_classifier.pkl')

