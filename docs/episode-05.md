# Episode 5: Building & Distribution

!!! clipboard-list "Learning Objectives"
    By the end of this episode, you will:
    
    - Build wheel and source distributions
    - Understand semantic versioning
    - Publish packages to PyPI
    - Set up GitHub Actions for CI/CD
    - Create basic documentation
    - Understand package metadata and README rendering

## 🎬 Taking kir-pydemo to the World

Sarah's `kir-pydemo` package is polished, tested, and ready! But how does she share it?

> "I want colleagues at other institutions to use this. How do I get it on PyPI so they can just `pip install kir-pydemo`? And how do I make sure each release is properly tested?"

**The solution?** Build distributions and set up automated publishing!

## 📦 Understanding Package Distribution

### Types of Distributions

Python packages can be distributed in two formats:

#### 1. Source Distribution (sdist)

A compressed archive (.tar.gz) of your source code:

```
kir-pydemo-0.1.0.tar.gz
├── src/
│   └── kir_pydemo/
├── tests/
├── pyproject.toml
├── README.md
└── LICENSE
```

- **Pros**: Works on any platform, includes everything
- **Cons**: Requires build tools, slower to install
- **When**: Fallback when wheels aren't available

#### 2. Wheel (.whl)

A pre-built package ready for installation:

```
kir_pydemo-0.1.0-py3-none-any.whl
```

- **Pros**: Fast installation, no build required
- **Cons**: May need platform-specific builds (for C extensions)
- **When**: Preferred format for distribution

The filename tells you:
```
kir_pydemo - 0.1.0 - py3 - none - any .whl
    |         |      |     |     |
  package  version  py3  no ABI universal
                         (pure Python)
```

## 🏗️ Building Your Package

### Step 1: Install Build Tools

<div class="dracula" markdown="1">
```py
uv pip install build twine
```
</div>

- **build**: Creates wheels and sdist
- **twine**: Uploads packages to PyPI

### Step 2: Build the Distributions

<div class="dracula" markdown="1">
```py
# Build both wheel and source distribution
python -m build

# Output:
# Successfully built kir_pydemo-0.1.0.tar.gz and kir_pydemo-0.1.0-py3-none-any.whl
```
</div>

This creates a `dist/` directory:

```
dist/
├── kir_pydemo-0.1.0-py3-none-any.whl
└── kir_pydemo-0.1.0.tar.gz
```

### Step 3: Check the Build

```bash
# Verify the distribution
twine check dist/*

# Output:
# Checking dist/kir_pydemo-0.1.0-py3-none-any.whl: PASSED
# Checking dist/kir_pydemo-0.1.0.tar.gz: PASSED
```

### Step 4: Test Install Locally

<div class="dracula" markdown="1">
```py
# Create a fresh virtual environment
python -m venv test-env
source test-env/bin/activate

# Install from the wheel
pip install dist/kir_pydemo-0.1.0-py3-none-any.whl

# Test it works
kir-pydemo gc-content ATGC
# Output: GC content: 50.00%

# Deactivate and cleanup
deactivate
rm -rf test-env
```
</div>

## 🔢 Semantic Versioning

Version numbers communicate compatibility and changes:

```
MAJOR.MINOR.PATCH
  |     |     |
  |     |     └─ Bug fixes (backwards compatible)
  |     └─────── New features (backwards compatible)
  └───────────── Breaking changes (NOT backwards compatible)
```

### Examples

- `0.1.0` → `0.1.1`: Fixed a bug
- `0.1.1` → `0.2.0`: Added new feature (reverse_complement)
- `0.2.0` → `1.0.0`: First stable release
- `1.0.0` → `2.0.0`: Changed API (breaking change)

### Pre-releases

```
1.0.0a1   # Alpha release 1
1.0.0b1   # Beta release 1
1.0.0rc1  # Release candidate 1
1.0.0     # Final release
```

### Version in pyproject.toml

**Static version:**
```toml
[project]
version = "0.1.0"
```

**Dynamic version** (from code):
```toml
[project]
dynamic = ["version"]

[tool.setuptools.dynamic]
version = {attr = "kir_pydemo.__version__"}
```

Then in `src/kir_pydemo/__init__.py`:
```python
__version__ = "0.1.0"
```

!!! tip "Version Management Tools"
    - **bump2version**: CLI tool to bump versions
    - **poetry version**: Poetry's version management
    - **setuptools_scm**: Git tag-based versioning
    
    Example with setuptools_scm:
    ```toml
    [build-system]
    requires = ["setuptools>=61.0", "setuptools-scm"]
    
    [project]
    dynamic = ["version"]
    
    [tool.setuptools_scm]
    ```

## 🚀 Publishing to PyPI

### Test on TestPyPI First

[TestPyPI](https://test.pypi.org/) is a separate instance for testing:

```bash
# Create account on https://test.pypi.org/account/register/

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Install from TestPyPI to verify
pip install --index-url https://test.pypi.org/simple/ kir-pydemo
```

### Publish to PyPI

```bash
# Create account on https://pypi.org/account/register/

# Upload to PyPI
twine upload dist/*

# Enter your credentials or use API token
```

!!! warning "Package Name Availability"
    Check if the name is available first:
    ```bash
    pip search kir-pydemo  # Deprecated, use web search instead
    ```
    Visit https://pypi.org/project/ to check.

### Using API Tokens (Recommended)

Create an API token on PyPI:

1. Go to https://pypi.org/manage/account/
2. Create a new API token
3. Store it safely

**Option 1: .pypirc file**

Create `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...

[testpypi]
username = __token__
password = pypi-AgENdGVzdC5weXBp...
```

**Option 2: Environment variable**

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmc...

twine upload dist/*
```

## 🤖 Continuous Integration with GitHub Actions

Automate testing and publishing with GitHub Actions:

### Step 1: Create Workflow Directory

```bash
mkdir -p .github/workflows
```

### Step 2: Create CI Workflow

Create `.github/workflows/ci.yml`:

<div class="nord" markdown="1">
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.9', '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    
    - name: Lint with ruff
      run: |
        ruff check src/ tests/
    
    - name: Type check with mypy
      run: |
        mypy src/
    
    - name: Test with pytest
      run: |
        pytest --cov=kir_pydemo --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```
</div>

### Step 3: Create Release Workflow

Create `.github/workflows/release.yml`:

<div class="nord" markdown="1">
```yaml
name: Release

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Check package
      run: twine check dist/*
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        twine upload dist/*
```
</div>

### Step 4: Add PyPI Token to GitHub

1. Generate API token on PyPI
2. Go to your GitHub repo → Settings → Secrets and variables → Actions
3. Add new secret: `PYPI_API_TOKEN`

Now when you create a release on GitHub, it automatically publishes to PyPI!

## 📚 Documentation

### README.md with Badges

Enhance your README with status badges:

```markdown
# kir-pydemo

[![CI](https://github.com/bmrc/kir-pydemo/workflows/CI/badge.svg)](https://github.com/bmrc/kir-pydemo/actions)
[![codecov](https://codecov.io/gh/bmrc/kir-pydemo/branch/main/graph/badge.svg)](https://codecov.io/gh/bmrc/kir-pydemo)
[![PyPI version](https://badge.fury.io/py/kir-pydemo.svg)](https://pypi.org/project/kir-pydemo/)
[![Python versions](https://img.shields.io/pypi/pyversions/kir-pydemo.svg)](https://pypi.org/project/kir-pydemo/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A demonstration package for DNA sequence analysis.

## Features

- Calculate GC content of DNA sequences
- Generate reverse complement of DNA sequences
- Command-line interface for quick analysis
- FASTA file support

## Installation

```bash
pip install kir-pydemo
```

With optional dependencies:
```bash
pip install kir-pydemo[bio]  # FASTA support
```

## Quick Start

```python
from kir_pydemo import gc_content, reverse_complement

# Calculate GC content
gc = gc_content("ATGCATGC")
print(f"GC content: {gc}%")  # GC content: 50.0%

# Get reverse complement
rev = reverse_complement("ATGC")
print(rev)  # GCAT
```

### Command Line

```bash
# Calculate GC content
kir-pydemo gc-content ATGCATGC

# Reverse complement
kir-pydemo reverse-complement ATGCATGC
```

## Documentation

Full documentation available at https://kir-pydemo......

## Contributing

Contributions welcome! Please read (Link to CONTRIBUTING.md)).

## License

MIT License - see (link to LICENSE) file.
```

### MkDocs Material Documentation

For modern, beautiful documentation, use [MkDocs Material](https://squidfunk.github.io/mkdocs-material/):

**Why MkDocs Material?**

- ✅ **Beautiful by default** - Professional appearance out of the box
- ✅ **Markdown-based** - Write docs in familiar Markdown format
- ✅ **Fast and responsive** - Works great on all devices
- ✅ **Easy to customize** - Simple YAML configuration
- ✅ **GitHub Pages ready** - Deploy with one command

#### Step 1: Install MkDocs Material

Add to your `pyproject.toml`:

```toml
[project.optional-dependencies]
docs = [
    "mkdocs-material>=9.5.0",
    "mkdocstrings[python]>=0.24.0",
]
```

Install:

```bash
pip install -e ".[docs]"
```

#### Step 2: Create Documentation Structure

```bash
# Initialize MkDocs
mkdocs new .

# This creates:
# mkdocs.yml          - Configuration file
# docs/
#   └── index.md      - Homepage
```

Create additional documentation pages:

```bash
mkdir -p docs/guide docs/api
touch docs/guide/installation.md
touch docs/guide/quickstart.md
touch docs/guide/cli.md
touch docs/api/reference.md
```

Your structure should look like:

```
kir-pydemo/
├── docs/
│   ├── index.md              # Homepage
│   ├── guide/
│   │   ├── installation.md   # Installation guide
│   │   ├── quickstart.md     # Quick start tutorial
│   │   └── cli.md            # CLI reference
│   └── api/
│       └── reference.md      # API documentation
├── mkdocs.yml                # MkDocs configuration
├── src/
└── pyproject.toml
```

#### Step 3: Configure mkdocs.yml

??? file-code "Create a comprehensive configuration:"

    ```yaml
    site_name: kir-pydemo
    site_description: DNA sequence analysis tools
    site_author: BMRC Training
    site_url: https://yourusername.github.io/kir-pydemo
    
    repo_name: yourusername/kir-pydemo
    repo_url: https://github.com/yourusername/kir-pydemo
    
    theme:
      name: material
      palette:
        # Light mode
        - scheme: default
          primary: indigo
          accent: indigo
          toggle:
            icon: material/brightness-7
            name: Switch to dark mode
        # Dark mode
        - scheme: slate
          primary: indigo
          accent: indigo
          toggle:
            icon: material/brightness-4
            name: Switch to light mode
      features:
        - navigation.tabs
        - navigation.sections
        - navigation.top
        - search.highlight
        - search.share
        - content.code.copy
        - content.code.annotate
    
    markdown_extensions:
      - pymdownx.highlight:
          anchor_linenums: true
      - pymdownx.inlinehilite
      - pymdownx.snippets
      - pymdownx.superfences
      - pymdownx.tabbed:
          alternate_style: true
      - admonition
      - pymdownx.details
    
    plugins:
      - search
      - mkdocstrings:
          handlers:
            python:
              paths: [src]
              options:
                docstring_style: numpy
                show_source: true
                show_root_heading: true
    
    nav:
      - Home: index.md
      - User Guide:
        - Installation: guide/installation.md
        - Quick Start: guide/quickstart.md
        - CLI Reference: guide/cli.md
      - API Reference: api/reference.md
    
    extra:
      social:
        - icon: fontawesome/brands/github
          link: https://github.com/yourusername/kir-pydemo
    ```
    
#### Step 4: Write Documentation Pages

**`docs/index.md`** (Homepage):

```markdown
# kir-pydemo

DNA sequence analysis tools for bioinformatics.

## Features

- 🧬 Calculate GC content of DNA sequences
- 🔄 Generate reverse complement
- 💻 Command-line interface
- 📁 FASTA file support

## Quick Example

```python
from kir_pydemo import gc_content, reverse_complement

# Calculate GC content
gc = gc_content("ATGCATGC")
print(f"GC content: {gc}%")  # 50.0%

# Reverse complement
rev = reverse_complement("ATGC")
print(rev)  # GCAT
```

## Installation

```bash
pip install kir-pydemo
```

For more details, see the (Link to Installation.MD or similar)).
```

**`docs/guide/installation.md`**:

```markdown
# Installation

## Basic Installation

Install kir-pydemo using pip:

```bash
pip install kir-pydemo
```

## Optional Dependencies

### FASTA Support

For reading FASTA files:

```bash
pip install kir-pydemo[bio]
```

### Development

For development with testing and linting tools:

```bash
pip install kir-pydemo[dev]
```

### All Features

Install everything:

```bash
pip install kir-pydemo[all]
```

## From Source

Clone and install from source:

```bash
git clone https://github.com/yourusername/kir-pydemo.git
cd kir-pydemo
pip install -e ".[dev]"
```
```

**`docs/api/reference.md`** (API Documentation with mkdocstrings):

```markdown
# API Reference

## Sequence Analysis

::: kir_pydemo.sequence
    options:
      show_root_heading: true
      show_source: true

## File I/O

::: kir_pydemo.io
    options:
      show_root_heading: true
      show_source: true
```

The `::: kir_pydemo.sequence` syntax automatically pulls docstrings from your code!

#### Step 5: Build and Serve Locally

```bash
# Serve locally with live reload
mkdocs serve

# Visit http://127.0.0.1:8000
```

Changes to your docs auto-reload in the browser!

```bash
# Build static site
mkdocs build

# Output goes to site/ directory
```

#### Step 6: Deploy to GitHub Pages

**Option 1: Manual deployment**

```bash
# Build and deploy to gh-pages branch
mkdocs gh-deploy
```

**Option 2: Automated with GitHub Actions**

Create `.github/workflows/docs.yml`:

```yaml
name: Documentation

on:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -e ".[docs]"
      
      - name: Deploy docs
        run: mkdocs gh-deploy --force
```

Now docs deploy automatically on every push to `main`!

**Enable GitHub Pages:**

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` / `root`
4. Save

Your docs will be live at: `https://yourusername.github.io/kir-pydemo`


## 📋 Complete Checklist for Release

!!! check-to-slot "Before publishing your package:"

    ### Code Quality
    - [ ] All tests passing
    - [ ] Code coverage >80%
    - [ ] No linting errors
    - [ ] Type checking passes
    - [ ] Pre-commit hooks configured
    
    ### Documentation
    - [ ] Comprehensive README.md
    - [ ] Usage examples
    - [ ] Installation instructions
    - [ ] API documentation
    - [ ] Changelog or release notes
    
    ### Metadata
    - [ ] Appropriate version number
    - [ ] Correct dependencies and version constraints
    - [ ] Proper license
    - [ ] Keywords and classifiers
    - [ ] Project URLs (homepage, docs, issues)
    
    ### Testing
    - [ ] Tested on multiple Python versions
    - [ ] Tested on different platforms (if relevant)
    - [ ] Test installation from built wheel
    
    ### Security
    - [ ] No sensitive data in code
    - [ ] Dependencies checked for vulnerabilities
    - [ ] API tokens secured (not in git)
    
    ### Legal
    - [ ] LICENSE file included
    - [ ] All code properly attributed
    - [ ] Dependencies' licenses compatible
    
    ## 📋 Checkpoint: What Have We Achieved?

Verify you've successfully completed Episode 5:

- [ ] Built wheel and source distributions with `python -m build`
- [ ] Verified distributions with `twine check`
- [ ] Understand semantic versioning (MAJOR.MINOR.PATCH)
- [ ] Published to TestPyPI successfully
- [ ] Set up GitHub Actions for CI
- [ ] Created comprehensive README with badges
- [ ] Configured automated release workflow

## 🎯 Key Takeaways

1. **Two distribution formats**: Wheels (preferred) and source distributions (fallback)
2. **Semantic versioning** communicates compatibility: MAJOR.MINOR.PATCH
3. **Test on TestPyPI** before publishing to PyPI
4. **Use API tokens** for secure authentication
5. **GitHub Actions** automate testing and publishing
6. **Good documentation** is crucial for adoption
7. **Release checklist** ensures quality releases

## 🎓 Series Wrap-Up

Congratulations! You've completed the Python Packaging Basics series. You now know how to:

✅ **Structure** packages with modern practices (src/ layout, pyproject.toml)  
✅ **Build** CLI tools with entry points  
✅ **Manage** dependencies and environments  
✅ **Test** and maintain code quality  
✅ **Distribute** packages to PyPI  

### What You've Built

The `kir-pydemo` package now:

- Has a clean, modern project structure
- Provides both Python API and CLI
- Manages dependencies properly
- Includes comprehensive tests
- Follows code quality standards
- Can be published to PyPI
- Has automated CI/CD

### Next Steps

- **Apply to your projects**: Package your own tools
- **Explore advanced topics**: C extensions, binary wheels, conda packages
- **Join the community**: Contribute to open source
- **Keep learning**: Python packaging evolves - stay updated!

## 📚 Further Reading

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Documentation](https://pypi.org/help/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Read the Docs](https://docs.readthedocs.io/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)


