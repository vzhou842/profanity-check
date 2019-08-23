import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="profanity-check",
  version="1.0.3",
  author="Victor Zhou",
  author_email="vzhou842@gmail.com",
  description="A fast, robust library to check for offensive language in strings.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/vzhou842/profanity-check",
  packages=setuptools.find_packages(),
  install_requires=['scikit-learn>=0.20.2'],
  package_data={ 'profanity_check': ['data/model.joblib', 'data/vectorizer.joblib'] },
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Natural Language :: English",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
