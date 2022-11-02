"""Setup"""
import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alt-profanity-check",
    version="1.1.3",
    author="Victor Zhou (original author), Menelaos Kotoglou, Dimitrios Mistriotis",
    author_email="dimitrios@mistriotis.com",
    description=(
        'Dropdown replacement of "profanity-check", '
        "A fast, robust library to check for offensive language in strings."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dimitrismistriotis/alt-profanity-check",
    packages=setuptools.find_packages(),
    install_requires=["scikit-learn==1.1.3", "joblib>=1.2.0"],
    python_requires=">=3.8",
    package_data={"profanity_check": ["data/model.joblib", "data/vectorizer.joblib"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["profanity_check=profanity_check.command_line:main"],
    },
)
