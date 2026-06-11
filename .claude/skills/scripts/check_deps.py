#!/usr/bin/env python3
"""
Check PyPI for latest versions of alt-profanity-check dependencies.
Compares with current versions in requirements.txt and setup.py.
"""

import json
import re
import sys
import urllib.request
from pathlib import Path


def get_pypi_version(package: str) -> str | None:
    """Fetch latest version of a package from PyPI."""
    url = f"https://pypi.org/pypi/{package}/json"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data["info"]["version"]
    except Exception as e:
        print(f"Error fetching {package}: {e}", file=sys.stderr)
        return None


def parse_requirements_txt(req_path: Path) -> dict[str, str]:
    """Extract pinned versions from requirements.txt."""
    if not req_path.exists():
        return {}

    versions = {}
    for line in req_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"([a-zA-Z0-9_-]+)==([^\s#]+)", line)
        if match:
            versions[match.group(1)] = match.group(2)
    return versions


def parse_setup_py(setup_path: Path) -> tuple[dict[str, str], str | None]:
    """Extract pinned versions and package version from setup.py."""
    if not setup_path.exists():
        return {}, None

    content = setup_path.read_text()

    # Extract package version
    pkg_version = None
    ver_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    if ver_match:
        pkg_version = ver_match.group(1)

    # Find install_requires section
    match = re.search(r"install_requires\s*=\s*\[(.*?)\]", content, re.DOTALL)
    if not match:
        return {}, pkg_version

    requires_block = match.group(1)
    versions = {}
    for pkg_match in re.finditer(r'"([a-zA-Z0-9_-]+)==([^"]+)"', requires_block):
        versions[pkg_match.group(1)] = pkg_match.group(2)

    return versions, pkg_version


def main():
    packages = ["scikit-learn", "joblib"]

    # Find project files
    cwd = Path.cwd()
    req_path = cwd / "requirements.txt"
    setup_path = cwd / "setup.py"

    req_versions = parse_requirements_txt(req_path)
    setup_versions, pkg_version = parse_setup_py(setup_path)

    # Prefer requirements.txt, fallback to setup.py
    current_versions = req_versions if req_versions else setup_versions

    print("=" * 60)
    print("alt-profanity-check Dependency Check")
    print("=" * 60)

    if pkg_version:
        print(f"\nCurrent package version: {pkg_version}")
    if req_path.exists():
        print(f"Reading from: {req_path}")
    if setup_path.exists():
        print(f"Reading from: {setup_path}")
    print()

    updates_available = []

    for pkg in packages:
        pypi_version = get_pypi_version(pkg)
        current = current_versions.get(pkg, "not found")

        needs_update = pypi_version and pypi_version != current
        status = "⚠ UPDATE AVAILABLE" if needs_update else "✓ up to date"

        if needs_update:
            updates_available.append((pkg, current, pypi_version))

        print(f"{pkg}:")
        print(f"  Current:  {current}")
        print(f"  Latest:   {pypi_version}")
        print(f"  Status:   {status}")
        print()

    if updates_available:
        new_sklearn = next(
            (v[2] for v in updates_available if v[0] == "scikit-learn"), None
        )

        print("=" * 60)
        print("ACTION REQUIRED")
        print("=" * 60)
        print()
        print("1. Update requirements.txt:")
        for pkg, _, latest in updates_available:
            print(f"   {pkg}=={latest}")
        print()
        print("2. Update setup.py install_requires to match")
        if new_sklearn:
            print(f"3. Bump version in setup.py to: {new_sklearn}")
        print()
        print("4. Set up venv and retrain models:")
        print("   python -m venv venv && source venv/bin/activate")
        print("   pip install -r requirements.txt -r development_requirements.txt")
        print("   cd profanity_check/data && python train_model.py")
        print()
        print("5. Run tests:")
        print("   python -m pytest --import-mode=append tests/")
        print()
        print("6. Update CHANGELOG.md")
        print("7. Commit, push, and create GitHub release")
    else:
        print("✓ All dependencies are up to date!")

    return 0 if not updates_available else 1


if __name__ == "__main__":
    sys.exit(main())
