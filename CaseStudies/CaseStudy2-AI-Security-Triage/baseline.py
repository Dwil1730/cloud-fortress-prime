from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
import pandas as pd

df = pd.read_csv('clean_tickets.csv')
X = df ['text'] # input: combined description
y = df ['Priority'] # target: High/Low/etc.

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_vec, y_train)

preds = model.predict(X_test_vec)
f1 = f1_score(y_test, preds, average='weighted')
print("Baseline F1 score:", round(f1, 3))
