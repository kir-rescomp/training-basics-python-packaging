# Episode 3: Dependencies & Environments

!!! info "Learning Objectives"
    By the end of this episode, you will:
    
    - Understand how to specify package dependencies
    - Use optional dependencies with "extras"
    - Work with virtual environments effectively
    - Handle version constraints properly
    - Understand the difference between package and development dependencies

## 🎬 Sarah's Growing Package

Dr. Sarah's `kir-pydemo` package is getting popular! Now she wants to add some new features:

- **Read FASTA files** (needs `biopython`)
- **Create plots** of GC content distributions (needs `matplotlib`)
- **Statistical analysis** of sequences (needs `numpy`, `scipy`)

But she has concerns:

> "Not everyone needs all these features. Do I force all users to install matplotlib even if they just want basic sequence analysis? What if someone's using an old version of numpy that conflicts with what I need?"

**The solution?** Proper dependency management with pyproject.toml!

## 📦 Understanding Dependencies

Dependencies are other Python packages that your package needs to work. There are different types:

### 1. Core Dependencies

**Required for basic functionality** - installed automatically with your package:

```toml
[project]
dependencies = [
    "biopython>=1.80",
    "numpy>=1.20.0",
]
```

### 2. Optional Dependencies

**Needed for extra features** - installed only when requested:

```toml
[project.optional-dependencies]
plotting = ["matplotlib>=3.5.0"]
dev = ["pytest>=7.0", "black>=22.0"]
```

Installed with: `pip install kir-pydemo[plotting]`

### 3. Development Dependencies

**Tools for development** - not needed by users:

- Testing frameworks (pytest)
- Code formatters (black, ruff)
- Documentation builders (sphinx)
- Type checkers (mypy)

## 🔨 Hands-On: Adding Dependencies

### Step 1: Decide What's Core vs. Optional

For `kir-pydemo`, let's say we want to add:

- **Core**: None (our basic functions use only stdlib!)
- **Optional - bio**: `biopython` for FASTA file support
- **Optional - plotting**: `matplotlib` for visualization
- **Optional - dev**: Testing and code quality tools

### Step 2: Update pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "kir-pydemo"
version = "0.2.0"  # 🆕 Bumped version
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

# 🆕 NEW: Optional dependencies
[project.optional-dependencies]
bio = [
    "biopython>=1.80",
]
plotting = [
    "matplotlib>=3.5.0",
    "numpy>=1.20.0",
]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
]
# Convenience: Install everything
all = [
    "kir-pydemo[bio,plotting]",
]

[project.scripts]
kir-pydemo = "kir_pydemo.cli:main"

[project.urls]
Homepage = "https://github.com/bmrc/kir-pydemo"
Documentation = "https://kir-pydemo.readthedocs.io"
Repository = "https://github.com/bmrc/kir-pydemo"
Issues = "https://github.com/bmrc/kir-pydemo/issues"
```

### Step 3: Version Constraints

Let's understand version specifiers:

```toml
dependencies = [
    "numpy",                    # Any version (not recommended!)
    "numpy>=1.20.0",           # Minimum version
    "numpy>=1.20.0,<2.0.0",    # Version range
    "numpy~=1.20.0",           # Compatible release (>=1.20.0, <1.21.0)
    "numpy==1.20.0",           # Exact version (too restrictive!)
]
```

**Best practices:**

- ✅ Use minimum versions: `package>=1.0.0`
- ✅ Exclude known broken versions: `package>=1.0.0,!=1.2.0`
- ✅ Use upper bounds cautiously: `package>=1.0.0,<2.0.0`
- ❌ Avoid pinning exact versions in libraries: `package==1.0.0`

!!! warning "Pinning vs. Constraints"
    **Libraries** (packages imported by others) should use loose constraints:
    ```toml
    dependencies = ["requests>=2.28.0"]
    ```
    
    **Applications** (final products) can pin exact versions:
    ```toml
    dependencies = ["requests==2.31.0"]
    ```
    
    `kir-pydemo` is a library, so we use minimum version constraints.

### Step 4: Add FASTA Support

Create a new module `src/kir_pydemo/io.py` that uses biopython:

```python
"""File I/O utilities for sequence data."""

from pathlib import Path
from typing import List, Tuple

try:
    from Bio import SeqIO
    HAS_BIOPYTHON = True
except ImportError:
    HAS_BIOPYTHON = False


def read_fasta(filepath: Path) -> List[Tuple[str, str]]:
    """
    Read sequences from a FASTA file.
    
    Parameters
    ----------
    filepath : Path
        Path to the FASTA file
    
    Returns
    -------
    List[Tuple[str, str]]
        List of (name, sequence) tuples
    
    Raises
    ------
    ImportError
        If biopython is not installed
    FileNotFoundError
        If the file doesn't exist
    
    Examples
    --------
    >>> sequences = read_fasta(Path("sequences.fasta"))
    >>> for name, seq in sequences:
    ...     print(f"{name}: {len(seq)} bp")
    """
    if not HAS_BIOPYTHON:
        raise ImportError(
            "biopython is required for FASTA support. "
            "Install with: pip install kir-pydemo[bio]"
        )
    
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    sequences = []
    for record in SeqIO.parse(filepath, "fasta"):
        sequences.append((record.id, str(record.seq)))
    
    return sequences
```

!!! tip "Graceful Degradation"
    Notice the pattern:
    
    1. Try to import optional dependency
    2. Set a `HAS_*` flag
    3. Check the flag before using the feature
    4. Raise helpful error if not installed
    
    This allows users to install only what they need!

### Step 5: Update CLI for FASTA Support

Update `src/kir_pydemo/cli.py` to support FASTA files:

```python
# Add to the gc-content subcommand
gc_parser.add_argument(
    "--fasta",
    type=Path,
    help="read sequences from FASTA file (requires: pip install kir-pydemo[bio])",
)
```

```python
# In cmd_gc_content function
def cmd_gc_content(args: argparse.Namespace) -> int:
    """Handle the gc-content command."""
    sequences = []
    
    if args.fasta:
        try:
            from kir_pydemo.io import read_fasta
            fasta_sequences = read_fasta(args.fasta)
            for name, seq in fasta_sequences:
                result = gc_content(seq)
                print(f"{name}: GC content = {result:.{args.precision}f}%")
            return 0
        except ImportError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    # ... rest of the function
```

## 🌍 Virtual Environments

Virtual environments isolate your project's dependencies from the system Python.

### Why Use Virtual Environments?

**Without virtual environments:**
```
System Python
├── numpy==1.19.0  (old project needs this)
├── pandas==1.3.0
└── kir-pydemo attempts to install numpy>=1.20.0  ❌ CONFLICT!
```

**With virtual environments:**
```
System Python
└── virtualenv installed

Project A (venv-a/)
├── numpy==1.19.0
└── pandas==1.3.0

Project B (venv-b/)
├── numpy==1.23.0  ✅ No conflict!
└── kir-pydemo
```

### Creating Virtual Environments

#### Using venv (built-in)

```bash
# Create a virtual environment
python -m venv venv

# Activate it
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Your prompt changes: (venv) user@host:~$

# Install packages in this environment
pip install -e ".[dev]"

# Deactivate when done
deactivate
```

#### Using conda

```bash
# Create environment with specific Python version
conda create -n kir-pydemo python=3.11

# Activate
conda activate kir-pydemo

# Install package
pip install -e ".[dev]"

# Deactivate
conda deactivate
```

### Installing with Extras

```bash
# Install just the package
pip install kir-pydemo

# Install with bio support
pip install kir-pydemo[bio]

# Install with multiple extras
pip install kir-pydemo[bio,plotting]

# Install everything
pip install kir-pydemo[all]

# For development (editable install with dev tools)
pip install -e ".[dev]"
```

!!! note "Quote the Extras"
    On some shells (especially zsh), you need quotes:
    ```bash
    pip install "kir-pydemo[bio]"   # Quoted
    pip install -e ".[dev]"         # Quoted
    ```

## 📝 requirements.txt vs pyproject.toml

People often ask: "Should I use requirements.txt or pyproject.toml?"

### pyproject.toml (for libraries)

```toml
[project]
dependencies = [
    "numpy>=1.20.0",  # Loose constraints
]
```

**Use when:**

- Building a package to distribute
- Want to specify minimum requirements
- Need flexibility for users

### requirements.txt (for applications)

```
# requirements.txt
numpy==1.23.4      # Pinned versions
pandas==1.5.3
matplotlib==3.7.1
```

**Use when:**

- Deploying an application
- Need reproducible environments
- Want exact versions

### Both Together

For `kir-pydemo` development, you might have:

**pyproject.toml** - Loose constraints for users:
```toml
[project]
dependencies = ["numpy>=1.20.0"]

[project.optional-dependencies]
dev = ["pytest>=7.0"]
```

**requirements-dev.txt** - Pinned versions for development:
```
# Exact versions used in development
numpy==1.23.4
pytest==7.4.0
black==23.7.0
```

Generate from current environment:
```bash
pip freeze > requirements-dev.txt
```

## 🔒 Dependency Lock Files

Modern tools provide lock files for reproducible installs:

### Poetry (poetry.lock)

```bash
# Install poetry
pip install poetry

# Initialize
poetry init

# Add dependency
poetry add numpy

# Generates poetry.lock with exact versions
```

### PDM (pdm.lock)

```bash
# Install pdm
pip install pdm

# Initialize
pdm init

# Add dependency
pdm add numpy

# Generates pdm.lock
```

### pip-tools (requirements.txt + requirements.in)

```bash
# Install pip-tools
pip install pip-tools

# Create requirements.in (loose)
echo "numpy>=1.20.0" > requirements.in

# Generate requirements.txt (pinned)
pip-compile requirements.in

# Install exact versions
pip-sync requirements.txt
```

!!! info "Lock Files in Practice"
    For `kir-pydemo` (a library), we don't commit lock files to the repository. For applications, lock files ensure everyone uses identical dependency versions.

## 📋 Checkpoint: What Have We Achieved?

Verify you've successfully completed Episode 3:

- [ ] Added optional dependencies to `pyproject.toml`
- [ ] Created extras: `[bio]`, `[plotting]`, `[dev]`, `[all]`
- [ ] Implemented graceful dependency handling with try/except
- [ ] Added FASTA file support with biopython
- [ ] Created and activated a virtual environment
- [ ] Installed package with extras: `pip install -e ".[dev]"`
- [ ] Understand version constraints and when to use them

## 🎯 Key Takeaways

1. **Dependencies** in `[project.dependencies]` are always installed
2. **Optional dependencies** in `[project.optional-dependencies]` are installed with `[extras]`
3. **Version constraints** should be loose for libraries, strict for applications
4. **Virtual environments** isolate project dependencies
5. **Graceful degradation** provides helpful errors when optional deps are missing
6. **Lock files** ensure reproducible environments (more important for apps than libraries)

## 🚀 What's Next?

In Episode 4, we'll add **Testing & Quality** tools to ensure kir-pydemo is reliable and maintainable:

- Writing tests with pytest
- Code formatting with black/ruff  
- Type checking with mypy
- Pre-commit hooks for automation

This will make your package production-ready!

## 📚 Further Reading

- [Dependency Specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/)
- [Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Poetry Documentation](https://python-poetry.org/)
- [PDM Documentation](https://pdm.fming.dev/)

---

**Previous:** [← Episode 2: Entry Points](episode-02.md) | **Next:** [Episode 4: Testing & Quality →](episode-04.md)
