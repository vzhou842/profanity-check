---
name: alt-profanity-check-deps
description: Dependency update workflow for alt-profanity-check Python package. Use when checking for updates to scikit-learn (primary dependency that drives versioning), joblib, or other dependencies. Handles PyPI version checking, requirements.txt/setup.py updates, virtual environment setup, model retraining, testing, changelog updates, version bumping, and release preparation. Trigger on requests like "check for dependency updates", "update scikit-learn version", "prepare new release", or "retrain models".
---

# alt-profanity-check Dependency Update Workflow

## Version Coupling

alt-profanity-check version = scikit-learn version (e.g., scikit-learn 1.8.0 → alt-profanity-check 1.8.0)

## Key Files

- `requirements.txt` - Runtime dependencies (scikit-learn, joblib)
- `setup.py` - Package version and install_requires
- `development_requirements.txt` - Test/dev dependencies
- `profanity_check/data/train_model.py` - Model retraining script
- `CHANGELOG.md` - Release notes

## Full Update Workflow

### 1. Check PyPI for Latest Versions

```bash
# scikit-learn
curl -s https://pypi.org/pypi/scikit-learn/json | python3 -c "import sys,json; print(json.load(sys.stdin)['info']['version'])"

# joblib
curl -s https://pypi.org/pypi/joblib/json | python3 -c "import sys,json; print(json.load(sys.stdin)['info']['version'])"
```

Or run: `scripts/check_deps.py`

### 2. Update Dependency Files

Update `requirements.txt`:
```
scikit-learn==1.8.0
joblib==1.5.3
```

Update `setup.py` install_requires to match:
```python
install_requires=[
    "scikit-learn==1.8.0",
    "joblib==1.5.3",
]
```

### 3. Bump Package Version in setup.py

Update version to match scikit-learn:
```python
version="1.8.0",
```

### 4. Set Up Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
pip install -r development_requirements.txt
```

### 5. Retrain Models

Models MUST be retrained with the new scikit-learn version:

```bash
cd profanity_check/data
python train_model.py
```

This regenerates:
- `profanity_check/data/model.joblib`
- `profanity_check/data/vectorizer.joblib`

### 6. Run Tests

```bash
python -m pytest --import-mode=append tests/
```

### 7. Update CHANGELOG.md

Add entry at top:
```markdown
## 1.8.0 - YYYY-MM-DD

- Updated scikit-learn to 1.8.0
- Updated joblib to 1.5.3
- Python >= 3.11 required (scikit-learn 1.8 requirement)
- Retrained models with scikit-learn 1.8.0
```

