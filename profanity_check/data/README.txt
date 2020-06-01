The original joblib files were dumped using joblib imports from sklearn. This gives the following error in Python 3.6 and later:
E   ModuleNotFoundError: No module named 'sklearn.externals.joblib'

See https://travis-ci.com/github/vzhou842/profanity-check for details.

The fix for this is to open the joblib files in Python 3.5, then dumping them using joblib. This gives the *_35.joblib files.

These are then loaded and dumped in Python3.7, so that there are no compatibility warnings. This gives the *_37.joblib files.

Finally, the files without any versioning should be considered the “latest” files. model.joblib and vectorizer.joblib are the files saved using joblib in Python3.7. These should be updated as the versions of Python get updated.


