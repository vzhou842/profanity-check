"""Train Model from data"""
import subprocess
from pathlib import Path

# import pandas as pd
# from joblib import dump
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.svm import LinearSVC
# from sklearn.calibration import CalibratedClassifierCV

DATA_FILE_NAME = "clean_data.csv"

# data = pd.read_csv(DATA_FILE)
# texts = data["text"].astype(str)
# y = data["is_offensive"]
#
# vectorizer = TfidfVectorizer(stop_words="english", min_df=0.0001)
# X = vectorizer.fit_transform(texts)
#
# model = LinearSVC(class_weight="balanced", dual=False, tol=1e-2, max_iter=int(1e5))
# calibrated_classifier_cv = CalibratedClassifierCV(estimator=model)
# calibrated_classifier_cv.fit(X, y)
#
# dump(vectorizer, "vectorizer.joblib")
# dump(calibrated_classifier_cv, "model.joblib")

if __name__ == "__main__":
    print()
    print("Training model")
    print()

    data_file = Path(__file__).parent / DATA_FILE_NAME
    if not data_file.exists():
        print(f"Could not find {DATA_FILE_NAME}, will try to extract.")
        subprocess.run(["./decompress_data"])

