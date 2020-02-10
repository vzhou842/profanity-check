import pkg_resources
import joblib

vectorizer = joblib.load(pkg_resources.resource_filename('profanity_check', 'data/vectorizer.joblib'))
model = joblib.load(pkg_resources.resource_filename('profanity_check', 'data/model.joblib'))

def _get_profane_prob(prob):
  return prob[1]

def predict(texts):
  return model.predict(vectorizer.transform(texts))

def predict_prob(texts):
  return [_get_profane_prob(i) for i in model.predict_proba(vectorizer.transform(texts))]
