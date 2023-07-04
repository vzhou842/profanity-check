"""Train Model from data"""
import hashlib
import subprocess
from pathlib import Path

import pandas as pd
from joblib import dump
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

DATA_FILE_NAME = "clean_data.csv"
HASH_OF_DATA_FILE = f"{DATA_FILE_NAME}.sha512"


def sha256sum(filename) -> str:
    """Compute SHA256 hash of file

    Helper method from StackOverflow: https://stackoverflow.com/a/44873382
    """
    with open(filename, "rb", buffering=0) as f:
        return hashlib.file_digest(f, "sha512").hexdigest()


if __name__ == "__main__":
    print()
    print("Training model")
    print()

    data_file = Path(__file__).parent / DATA_FILE_NAME
    if not data_file.exists():
        print(f"Could not find {DATA_FILE_NAME}, will try to extract.")
        subprocess.run(["./decompress_data"])

        hash_sha512 = sha256sum(data_file)
        hash_file = Path(__file__).parent / HASH_OF_DATA_FILE
        stored_hash = hash_file.read_text().strip().split(" ")[0]
        print(stored_hash)

        print()
        print(f"SHA512 hash of {DATA_FILE_NAME}: {hash_sha512}")
        print(f"Stored hash to check against: {stored_hash}")
        print()

        assert hash_sha512 == stored_hash, (
            f"Hash of {DATA_FILE_NAME} does not match stored hash. "
            "Please download the data again."
        )

    data = pd.read_csv(DATA_FILE_NAME)
    texts = data["text"].astype(str)
    y = data["is_offensive"]

    vectorizer = TfidfVectorizer(stop_words="english", min_df=0.0001)
    X = vectorizer.fit_transform(texts)

    model = LinearSVC(class_weight="balanced", dual=False, tol=1e-2, max_iter=int(1e5))
    calibrated_classifier_cv = CalibratedClassifierCV(estimator=model)
    calibrated_classifier_cv.fit(X, y)

    dump(vectorizer, "vectorizer.joblib")
    dump(calibrated_classifier_cv, "model.joblib")
