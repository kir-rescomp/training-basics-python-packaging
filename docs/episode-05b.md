# Episode 05.b - Building and Distribution 

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