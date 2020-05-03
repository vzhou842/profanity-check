from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC

data_path = Path(__file__).parent / "data"

# Read in data:
clean_data_location = data_path / "clean_data.csv"
data = pd.read_csv(clean_data_location)
texts = data["text"].astype(str)
y = data["is_offensive"]

# Vectorize the text:
vectorizer = CountVectorizer(stop_words="english", min_df=0.0001)
X = vectorizer.fit_transform(texts)

# Train the model:
model = LinearSVC(class_weight="balanced", dual=False, tol=1e-2, max_iter=1e5)
cclf = CalibratedClassifierCV(base_estimator=model)
cclf.fit(X, y)

# Save the model:
vectorizer_location = data_path / "vectorizer.joblib"
joblib.dump(vectorizer, vectorizer_location)
model_location = data_path / "model.joblib"
joblib.dump(cclf, model_location)
