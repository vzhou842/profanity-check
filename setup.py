"""
Setup file for the package hanzo-profanity-check.
This is forked from https://github.com/vzhou842/profanity-check .
"""

import setuptools


with open("README.md", "r") as file_handle:
    long_description = file_handle.read()

setuptools.setup(
    name="hanzo-profanity-check",
    version="1.0",
    # use_scm_version=True,

    author="Hanzo Archives",
    author_email="hanzo-dev@hanzoarchives.com",

    description="Forked copy of profanity-check",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hanzoarchives/profanity-check",

    packages=setuptools.find_packages(),

    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: Linux",
    ],

    install_requires=[
        'joblib>=0.14.1',
        'scikit-learn>=0.20.2'
    ],

    package_data={
        'profanity_check': [
            'data/model.joblib',
            'data/vectorizer.joblib'
        ]
    },

    tests_require=[
        'flake8',
        'pytest',
        'pylint',
        'mock'
    ],

    setup_requires=[
        'pytest-runner',
        'pytest-pylint',
        'flake8',
        'setuptools_scm',
        'wheel'
    ]
)
