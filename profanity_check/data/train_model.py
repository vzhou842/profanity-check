"""Train Model from data"""
import pandas as pd
from joblib import dump
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

data = pd.read_csv("clean_data.csv")
texts = data["text"].astype(str)
y = data["is_offensive"]

vectorizer = TfidfVectorizer(stop_words="english", min_df=0.0001)
X = vectorizer.fit_transform(texts)

model = LinearSVC(class_weight="balanced", dual=False, tol=1e-2, max_iter=1e5)
calibrated_classifier_cv = CalibratedClassifierCV(base_estimator=model)
calibrated_classifier_cv.fit(X, y)

dump(vectorizer, "vectorizer.joblib")
dump(calibrated_classifier_cv, "model.joblib")
