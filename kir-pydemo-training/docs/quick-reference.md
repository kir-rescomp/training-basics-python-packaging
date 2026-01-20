# Quick Reference Guide

A cheat sheet for Python packaging tasks covered in this training series.

## 📦 Project Structure

```
kir-pydemo/
├── src/
│   └── kir_pydemo/
│       ├── __init__.py
│       ├── sequence.py
│       ├── cli.py
│       └── io.py
├── tests/
│   ├── test_sequence.py
│   └── test_cli.py
├── docs/
│   └── ...
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── Makefile
├── pyproject.toml
└── README.md
```

## ⚙️ pyproject.toml Template

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "your-package"
version = "0.1.0"
description = "Short description"
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "email@example.com"}
]
keywords = ["keyword1", "keyword2"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "package1>=1.0.0",
    "package2>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
]
docs = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.3.0",
]

[project.scripts]
your-cli = "your_package.cli:main"

[project.urls]
Homepage = "https://github.com/username/your-package"
Documentation = "https://your-package.readthedocs.io"
Repository = "https://github.com/username/your-package"
Issues = "https://github.com/username/your-package/issues"

[tool.black]
line-length = 100
target-version = ["py39", "py310", "py311", "py312"]

[tool.ruff]
line-length = 100
target-version = "py39"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "C4", "UP"]
ignore = ["E501"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = ["--strict-markers", "-ra"]

[tool.coverage.run]
source = ["your_package"]
omit = ["*/tests/*"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

## 🔧 Common Commands

### Virtual Environments

```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Deactivate
deactivate
```

### Installation

```bash
# Install package in editable mode
pip install -e .

# Install with extras
pip install -e ".[dev]"
pip install -e ".[dev,docs]"

# Install from PyPI
pip install kir-pydemo

# Install specific version
pip install kir-pydemo==0.1.0
```

### Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_sequence.py

# Run with coverage
pytest --cov=your_package

# Generate HTML coverage report
pytest --cov=your_package --cov-report=html

# Run tests matching pattern
pytest -k "gc_content"
```

### Code Quality

```bash
# Format with black
black src/ tests/

# Format with ruff
ruff format src/ tests/

# Lint with ruff
ruff check src/ tests/

# Fix auto-fixable issues
ruff check --fix src/ tests/

# Type check with mypy
mypy src/

# Run all quality checks
black src/ tests/ && ruff check --fix src/ tests/ && mypy src/ && pytest
```

### Pre-commit

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run on all files
pre-commit run --all-files

# Update hook versions
pre-commit autoupdate
```

### Building & Publishing

```bash
# Install build tools
pip install build twine

# Build distributions
python -m build

# Check distributions
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Clean build artifacts
rm -rf build dist *.egg-info
```

### Git & Version Control

```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit"

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Testing
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.ruff_cache/

# Build
build/
dist/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF

# Tag a release
git tag v0.1.0
git push origin v0.1.0
```

## 📝 Version Specifiers

```toml
dependencies = [
    "package",              # Any version (not recommended)
    "package==1.0.0",       # Exactly version 1.0.0
    "package>=1.0.0",       # Version 1.0.0 or higher
    "package<=1.0.0",       # Version 1.0.0 or lower
    "package~=1.0.0",       # Compatible release (>=1.0.0, <1.1.0)
    "package>=1.0,<2.0",    # Version range
    "package>=1.0,!=1.2.0", # Exclude specific version
]
```

**Best practices:**
- Libraries: Use loose constraints (`>=1.0.0`)
- Applications: Can pin exact versions (`==1.0.0`)

## 🎯 Entry Points

### Console Scripts

```toml
[project.scripts]
my-cli = "package.module:function"
```

**Example:**
```python
# In package/cli.py
def main():
    print("Hello from CLI")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### Multiple Commands

```toml
[project.scripts]
pkg-cmd1 = "package.cli:cmd1"
pkg-cmd2 = "package.cli:cmd2"
```

## 🧪 pytest Fixtures

```python
import pytest

@pytest.fixture
def sample_sequence():
    """Provide a sample DNA sequence for testing."""
    return "ATGCATGC"

def test_with_fixture(sample_sequence):
    assert len(sample_sequence) == 8
```

### Parametrized Tests

```python
@pytest.mark.parametrize("sequence,expected", [
    ("ATGC", 50.0),
    ("AAAA", 0.0),
    ("GGGG", 100.0),
])
def test_gc_content(sequence, expected):
    assert gc_content(sequence) == expected
```

## 📊 Semantic Versioning

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

**Examples:**
- `0.1.0` → `0.1.1`: Bug fix
- `0.1.1` → `0.2.0`: New feature
- `0.2.0` → `1.0.0`: First stable or breaking change
- `1.0.0` → `2.0.0`: Breaking change

**Pre-releases:**
- `1.0.0a1`: Alpha
- `1.0.0b1`: Beta
- `1.0.0rc1`: Release candidate

## 🔒 .gitignore Template

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
*.so

# Distribution / packaging
build/
dist/
*.egg-info/
*.egg

# Virtual environments
venv/
env/
ENV/

# Testing
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.ruff_cache/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

## 🪝 .pre-commit-config.yaml Template

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.13
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
```

## 🤖 GitHub Actions CI Template

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.9', '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
    
    - name: Run tests
      run: |
        pytest --cov=your_package
```

## 📚 Common PyPI Classifiers

```toml
classifiers = [
    # Development Status
    "Development Status :: 3 - Alpha",
    "Development Status :: 4 - Beta",
    "Development Status :: 5 - Production/Stable",
    
    # Intended Audience
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    
    # License
    "License :: OSI Approved :: MIT License",
    "License :: OSI Approved :: Apache Software License 2.0",
    "License :: OSI Approved :: BSD License",
    
    # Programming Language
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    
    # Topic
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]
```

Full list: https://pypi.org/classifiers/

## 🛠️ Makefile Template

```makefile
.PHONY: install test coverage format lint type-check clean build publish

install:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

coverage:
	pytest --cov=your_package --cov-report=html --cov-report=term

format:
	black src/ tests/
	ruff check --fix src/ tests/

lint:
	ruff check src/ tests/

type-check:
	mypy src/

clean:
	rm -rf build dist *.egg-info
	rm -rf htmlcov .coverage
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +

build: clean
	python -m build

publish-test: build
	twine upload --repository testpypi dist/*

publish: build
	twine upload dist/*

all: format lint type-check test
```

## 🔗 Useful Resources

### Official Documentation
- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI](https://pypi.org/)
- [setuptools](https://setuptools.pypa.io/)
- [pytest](https://docs.pytest.org/)

### Tools
- [Black](https://black.readthedocs.io/) - Code formatter
- [Ruff](https://docs.astral.sh/ruff/) - Fast linter
- [mypy](http://mypy-lang.org/) - Type checker
- [pre-commit](https://pre-commit.com/) - Git hooks
- [Sphinx](https://www.sphinx-doc.org/) - Documentation

### Version Control
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

### CI/CD
- [GitHub Actions](https://docs.github.com/en/actions)
- [Read the Docs](https://readthedocs.org/)
- [Codecov](https://about.codecov.io/)

---

**Back to:** [Home](index.md)
