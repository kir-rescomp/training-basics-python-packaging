# Episode 1: Project Structure & pyproject.toml

!!! clipboard-list "Learning Objectives"
    By the end of this episode, you will:
    
    - Understand what Python packaging is and why it matters
    - Know the modern approach using `pyproject.toml`
    - Set up a proper project structure with the `src/` layout
    - Create your first installable Python package
    - Install and test your package in editable mode

<div class="dracula" markdown="1">

## 🎬 The Story Begins

Meet **Dr. Sarah**, a bioinformatics researcher who has written some useful Python functions for DNA sequence analysis. Currently, her code looks like this:

```python
# sequence_utils.py
def gc_content(sequence):
    """Calculate GC content of a DNA sequence."""
    sequence = sequence.upper()
    g_count = sequence.count('G')
    c_count = sequence.count('C')
    return (g_count + c_count) / len(sequence) * 100

def reverse_complement(sequence):
    """Get reverse complement of a DNA sequence."""
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join(complement.get(base, base) for base in reversed(sequence.upper()))
```

Sarah copies this file into each new analysis project. But there are problems:

- **No version control** - Which version is the latest?
- **Code duplication** - Changes must be made everywhere
- **Hard to share** - Colleagues can't easily use her functions
- **No discoverability** - Others don't know these tools exist

**The solution?** Package it! Let's help Sarah transform her scripts into `kir-pydemo`, a proper Python package.

## 📦 What is Python Packaging?

Python packaging is the process of bundling your code so it can be:

- **Installed** with `pip install`
- **Imported** in any Python script: `import kir_pydemo`
- **Versioned** and tracked
- **Shared** with colleagues or the world
- **Managed** with proper dependencies

## 🏗️ Modern Python Packaging: The Evolution

### The Old Way: setup.py

Previously, Python packages used `setup.py`:

```python
# setup.py (old approach - don't use this!)
from setuptools import setup, find_packages

setup(
    name="kir-pydemo",
    version="0.1.0",
    packages=find_packages(),
    # ... more configuration
)
```

**Problems with setup.py:**

- Mixes configuration with executable code
- Different tools had different formats
- Security concerns (executes arbitrary Python)
- Hard to parse by automated tools

### The Modern Way: pyproject.toml

**PEP 517** and **PEP 518** introduced `pyproject.toml`, a declarative, standardized format:

```toml
# pyproject.toml (modern approach - use this!)
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "kir-pydemo"
version = "0.1.0"
```

**Benefits:**

- ✅ Declarative and readable (TOML format)
- ✅ Standardized across the Python ecosystem
- ✅ Safer (no code execution)
- ✅ Tool-independent
- ✅ Can include configuration for linters, formatters, etc.

!!! tip "Why TOML?"
    TOML (Tom's Obvious, Minimal Language) is designed for configuration files. It's more human-readable than JSON and less ambiguous than YAML.

## 📂 Project Structure: The src/ Layout

There are two common project layouts. We'll use the **src/ layout** (recommended):

```py
kir-pydemo/
├── src/
│   └── kir_pydemo/          # Note: underscores in Python package names
│       ├── __init__.py
│       └── sequence.py
├── tests/
│   └── test_sequence.py
├── pyproject.toml
├── README.md
└── LICENSE
```

### Why src/ Layout?

The **src/ layout** has a key advantage: it prevents you from accidentally importing the development version of your package instead of the installed version.

**Without src/ (flat layout):**

```py
kir-pydemo/
├── kir_pydemo/          # ⚠️ Python might import this directly
│   ├── __init__.py
│   └── sequence.py
├── tests/
└── pyproject.toml
```

If you're in the project directory and run `python -c "import kir_pydemo"`, Python might import the local directory instead of the installed package. This can hide installation problems!

**With src/ layout:**

```py
kir-pydemo/
├── src/
│   └── kir_pydemo/      # ✅ Must be installed to import
│       ├── __init__.py
│       └── sequence.py
├── tests/
└── pyproject.toml
```

Now you **must** install the package to import it, catching installation issues early.

!!! circle-info "Package Name vs. Import Name"
    - **Package name** (for PyPI): Can use hyphens: `kir-pydemo`
    - **Import name** (in Python): Must use underscores: `kir_pydemo`
    
    ```bash
    pip install kir-pydemo      # Install with hyphens
    ```
    
    ```python
    import kir_pydemo           # Import with underscores
    ```

## 🔨 Hands-On: Creating Your Package

### Step 1: Create the Directory Structure

```bash
# Create the project directory
mkdir kir-pydemo
cd kir-pydemo

# Create the src layout
mkdir -p src/kir_pydemo
mkdir tests

# Create essential files
touch src/kir_pydemo/__init__.py
touch src/kir_pydemo/sequence.py
touch README.md
touch pyproject.toml
```

### Step 2: Write the Package Code

**`src/kir_pydemo/__init__.py`**

This file makes `kir_pydemo` a Python package. It can be empty, or we can expose our main functions:

```python
"""kir-pydemo: A demonstration package for DNA sequence analysis."""

__version__ = "0.1.0"

# Import main functions to make them easily accessible
from kir_pydemo.sequence import gc_content, reverse_complement

__all__ = ["gc_content", "reverse_complement"]
```

**`src/kir_pydemo/sequence.py`**

```python
"""DNA sequence analysis utilities."""


def gc_content(sequence: str) -> float:
    """
    Calculate GC content of a DNA sequence.
    
    Parameters
    ----------
    sequence : str
        DNA sequence containing A, T, G, C nucleotides
    
    Returns
    -------
    float
        GC content as a percentage (0-100)
    
    Examples
    --------
    >>> gc_content("ATGC")
    50.0
    >>> gc_content("AAAA")
    0.0
    """
    if not sequence:
        raise ValueError("Sequence cannot be empty")
    
    sequence = sequence.upper()
    g_count = sequence.count('G')
    c_count = sequence.count('C')
    
    return (g_count + c_count) / len(sequence) * 100


def reverse_complement(sequence: str) -> str:
    """
    Get the reverse complement of a DNA sequence.
    
    Parameters
    ----------
    sequence : str
        DNA sequence containing A, T, G, C nucleotides
    
    Returns
    -------
    str
        Reverse complement of the input sequence
    
    Examples
    --------
    >>> reverse_complement("ATGC")
    'GCAT'
    >>> reverse_complement("AAAA")
    'TTTT'
    """
    complement_map = {
        'A': 'T', 'T': 'A',
        'G': 'C', 'C': 'G',
        'a': 't', 't': 'a',
        'g': 'c', 'c': 'g'
    }
    
    return ''.join(complement_map.get(base, base) for base in reversed(sequence))
```

!!! tip "Type Hints and Docstrings"
    Notice we're using:
    
    - **Type hints** (`sequence: str`, `-> float`) - Makes code more readable and enables static analysis
    - **NumPy-style docstrings** - Standard format for scientific Python packages
    - **Examples in docstrings** - Can be tested with `doctest`

### Step 3: Create pyproject.toml

Now for the heart of our package - the `pyproject.toml` file:

**`pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "kir-pydemo"
version = "0.1.0"
description = "A demonstration package for DNA sequence analysis"
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
authors = [
    {name = "BMRC Training", email = "training@example.com"}
]
keywords = ["bioinformatics", "DNA", "sequence analysis", "tutorial"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[project.urls]
Homepage = "https://github.com/bmrc/kir-pydemo"
Documentation = "https://kir-pydemo.readthedocs.io"
Repository = "https://github.com/bmrc/kir-pydemo"
Issues = "https://github.com/bmrc/kir-pydemo/issues"
```

Let's break this down:

#### [build-system]

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

- **requires**: Tools needed to build your package (setuptools is the most common)
- **build-backend**: Which build system to use (setuptools, flit, poetry, hatch, etc.)

!!! info "Build Backends"
    While we use `setuptools` (the most common and compatible choice), alternatives include:
    
    - **flit**: Simpler, for pure Python packages
    - **hatch**: Modern, with environment management
    - **poetry**: Includes dependency management
    - **PDM**: Supports PEP 582
    
    For scientific packages, `setuptools` remains the standard.

#### [project]

This section contains your package metadata:

- **name**: Package name on PyPI (can use hyphens)
- **version**: Current version (we'll cover version management in Episode 5)
- **description**: One-line summary
- **readme**: Path to README file (supports .md, .rst, .txt)
- **requires-python**: Minimum Python version
- **license**: License information
- **authors**: List of authors with name and email
- **keywords**: For discoverability on PyPI
- **classifiers**: Standardized categories (see [PyPI classifiers](https://pypi.org/classifiers/))

### Step 4: Add a README

**`README.md`**

```markdown
# kir-pydemo

A demonstration package for DNA sequence analysis, created as part of the Python Packaging Basics training series.

## Features

- Calculate GC content of DNA sequences
- Generate reverse complement of DNA sequences

## Installation

```bash
pip install kir-pydemo
```

## Usage

```python
from kir_pydemo import gc_content, reverse_complement

# Calculate GC content
sequence = "ATGCATGC"
gc = gc_content(sequence)
print(f"GC content: {gc}%")  # Output: GC content: 50.0%

# Get reverse complement
rev_comp = reverse_complement(sequence)
print(f"Reverse complement: {rev_comp}")  # Output: Reverse complement: GCATGCAT
```

## License

MIT
```

### Step 5: Install in Editable Mode

Now comes the magic moment - installing your package!

```bash
# Make sure you're in the kir-pydemo directory
cd /path/to/kir-pydemo

# Install in editable mode
pip install -e .
```

The `-e` flag means **editable mode** (also called **development mode**):

- Changes to your source code are immediately reflected
- No need to reinstall after each change
- Perfect for development

!!! warning "Virtual Environments"
    It's best practice to use a virtual environment:
    
    ```bash
    # Create a virtual environment
    python -m venv venv
    
    # Activate it
    source venv/bin/activate  # On Linux/Mac
    venv\Scripts\activate     # On Windows
    
    # Now install
    pip install -e .
    ```
    
    We'll cover this more in Episode 3!

### Step 6: Test Your Package

Now test that everything works:

```python
# Open a Python interpreter from anywhere (not in the project directory!)
python

>>> from kir_pydemo import gc_content, reverse_complement
>>> gc_content("ATGCATGC")
50.0
>>> reverse_complement("ATGC")
'GCAT'
>>> import kir_pydemo
>>> kir_pydemo.__version__
'0.1.0'
```

Success! Your package is installed and importable from anywhere on your system.

## 📋 Checkpoint: What Have We Achieved?

Let's verify you've successfully completed Episode 1:

- [ ] Created a `src/kir_pydemo/` directory structure
- [ ] Written `__init__.py` with version and imports
- [ ] Implemented functions in `sequence.py` with type hints and docstrings
- [ ] Created `pyproject.toml` with proper metadata
- [ ] Installed the package with `pip install -e .`
- [ ] Successfully imported and used the package

## 🎯 Key Takeaways

1. **Modern packaging uses `pyproject.toml`**, not `setup.py`
2. **The src/ layout** prevents import confusion and catches installation issues
3. **Package names** (with hyphens) vs **import names** (with underscores) are different
4. **Editable mode** (`pip install -e .`) is perfect for development
5. **Type hints and docstrings** make your package professional and maintainable

## 🚀 What's Next?

In Episode 2, we'll add command-line interface (CLI) capabilities to kir-pydemo, allowing users to run our functions directly from the terminal:

```bash
kir-pydemo gc-content ATGCATGC
# Output: 50.0
```

This will introduce **entry points** and **console scripts** - making your package even more useful!

## 📚 Further Reading

- [PEP 517 - Build System Interface](https://peps.python.org/pep-0517/)
- [PEP 518 - pyproject.toml](https://peps.python.org/pep-0518/)
- [PyPA Packaging Guide](https://packaging.python.org/)
- [setuptools documentation](https://setuptools.pypa.io/)

</div>
---

**Next:** [Episode 2: Entry Points & CLI Tools →](episode-02.md)
