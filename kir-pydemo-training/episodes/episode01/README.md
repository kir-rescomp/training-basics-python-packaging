# kir-pydemo - Episode 1

A demonstration package for DNA sequence analysis, created as part of the Python Packaging Basics training series.

## Features

- Calculate GC content of DNA sequences
- Generate reverse complement of DNA sequences

## Installation

```bash
# Install in editable mode (from the episode01 directory)
pip install -e .
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

## Development

This is Episode 1 of the Python Packaging training. At this stage, the package includes:

- ✅ Basic project structure with src/ layout
- ✅ pyproject.toml configuration
- ✅ Core sequence analysis functions
- ✅ Type hints and docstrings

## What's Next?

In Episode 2, we'll add CLI capabilities to run these functions from the command line!

## License

MIT
