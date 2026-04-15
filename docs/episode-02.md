# Episode 2: Entry Points & CLI Tools

!!! info "Learning Objectives"
    By the end of this episode, you will:
    
    - Understand what entry points are and why they're useful
    - Create command-line interfaces (CLIs) for your package
    - Use argparse for command-line argument parsing
    - Configure console scripts in pyproject.toml
    - Build user-friendly CLI tools

## 🎬 Continuing Sarah's Story

Dr. Sarah's colleagues love the `kir-pydemo` package! But they have a request:

> "Sarah, it's great that we can import your functions in Python, but sometimes we just want to quickly analyze a sequence from the command line. Can we do that?"

Currently, they have to write a Python script every time:

```python
# analyze.py - Have to create this every time!
from kir_pydemo import gc_content
import sys

sequence = sys.argv[1]
result = gc_content(sequence)
print(result)
```

```bash
python analyze.py ATGCATGC
# Output: 50.0
```

**Wouldn't it be better if they could just run:**

```bash
kir-pydemo gc-content ATGCATGC
# Output: GC content: 50.0%
```

**The solution?** Add command-line interface (CLI) capabilities using **entry points**!

## 🔌 What are Entry Points?

**Entry points** are a mechanism for making Python functions executable from the command line. When you install a package with entry points, Python automatically creates executable scripts that can be run directly from your terminal.

### Types of Entry Points

1. **Console Scripts** (most common)
   - Create command-line executables
   - Example: `kir-pydemo`, `pytest`, `black`

2. **GUI Scripts** (for graphical applications)
   - Similar to console scripts but for GUI apps
   - On Windows, doesn't open a console window

3. **Plugin Entry Points** (for extensibility)
   - Allow other packages to discover and use your code
   - Used by frameworks like pytest, Sphinx

We'll focus on **console scripts** in this episode.

### How Entry Points Work

When you define a console script entry point:

```toml
[project.scripts]
kir-pydemo = "kir_pydemo.cli:main"
```

Python packaging tools will:

1. Create an executable script named `kir-pydemo`
2. When run, it calls the `main()` function in `kir_pydemo.cli`
3. Install it in your Python environment's `bin/` directory
4. Make it available from anywhere in your PATH

## 🏗️ Designing a CLI

Before coding, let's design what we want our CLI to do:

```bash
# Calculate GC content
kir-pydemo gc-content ATGCATGC
# Output: GC content: 50.0%

# Get reverse complement
kir-pydemo reverse-complement ATGCATGC
# Output: GCATGCAT

# Read from file
kir-pydemo gc-content --file sequences.txt

# Get help
kir-pydemo --help
kir-pydemo gc-content --help
```

This follows a **subcommand pattern** (like `git commit`, `git push`) which is common for tools with multiple operations.

## 🔨 Hands-On: Building the CLI

### Step 1: Create the CLI Module

Create a new file `src/kir_pydemo/cli.py`:

```python
"""Command-line interface for kir-pydemo."""

import argparse
import sys
from pathlib import Path

from kir_pydemo import gc_content, reverse_complement, __version__


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="kir-pydemo",
        description="DNA sequence analysis tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True,
        help="available commands",
    )
    
    # GC content subcommand
    gc_parser = subparsers.add_parser(
        "gc-content",
        help="calculate GC content of a DNA sequence",
    )
    gc_parser.add_argument(
        "sequence",
        nargs="?",
        help="DNA sequence to analyze",
    )
    gc_parser.add_argument(
        "-f", "--file",
        type=Path,
        help="read sequences from file (one per line)",
    )
    gc_parser.add_argument(
        "-p", "--precision",
        type=int,
        default=2,
        help="decimal precision for output (default: 2)",
    )
    
    # Reverse complement subcommand
    revcomp_parser = subparsers.add_parser(
        "reverse-complement",
        help="get reverse complement of a DNA sequence",
    )
    revcomp_parser.add_argument(
        "sequence",
        nargs="?",
        help="DNA sequence to reverse complement",
    )
    revcomp_parser.add_argument(
        "-f", "--file",
        type=Path,
        help="read sequences from file (one per line)",
    )
    
    return parser


def cmd_gc_content(args: argparse.Namespace) -> int:
    """Handle the gc-content command."""
    sequences = []
    
    # Get sequences from file or command line
    if args.file:
        if not args.file.exists():
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            return 1
        sequences = args.file.read_text().strip().split('\n')
    elif args.sequence:
        sequences = [args.sequence]
    else:
        print("Error: Provide a sequence or use --file", file=sys.stderr)
        return 1
    
    # Process each sequence
    for seq in sequences:
        seq = seq.strip()
        if not seq:
            continue
        
        try:
            result = gc_content(seq)
            print(f"GC content: {result:.{args.precision}f}%")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    return 0


def cmd_reverse_complement(args: argparse.Namespace) -> int:
    """Handle the reverse-complement command."""
    sequences = []
    
    # Get sequences from file or command line
    if args.file:
        if not args.file.exists():
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            return 1
        sequences = args.file.read_text().strip().split('\n')
    elif args.sequence:
        sequences = [args.sequence]
    else:
        print("Error: Provide a sequence or use --file", file=sys.stderr)
        return 1
    
    # Process each sequence
    for seq in sequences:
        seq = seq.strip()
        if not seq:
            continue
        print(reverse_complement(seq))
    
    return 0


def main() -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Dispatch to the appropriate command handler
    if args.command == "gc-content":
        return cmd_gc_content(args)
    elif args.command == "reverse-complement":
        return cmd_reverse_complement(args)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

!!! tip "CLI Design Principles"
    This CLI follows good practices:
    
    - **Exit codes**: Returns 0 for success, 1 for errors
    - **Error messages to stderr**: Uses `file=sys.stderr` for errors
    - **Help text**: Clear descriptions for all commands and options
    - **Version info**: `--version` flag shows package version
    - **Flexible input**: Accepts sequences directly or from files

### Step 2: Update pyproject.toml

Add the entry point configuration to `pyproject.toml`:

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

# 🆕 NEW: Console scripts entry point
[project.scripts]
kir-pydemo = "kir_pydemo.cli:main"

[project.urls]
Homepage = "https://github.com/bmrc/kir-pydemo"
Documentation = "https://kir-pydemo.readthedocs.io"
Repository = "https://github.com/bmrc/kir-pydemo"
Issues = "https://github.com/bmrc/kir-pydemo/issues"
```

The key addition is:

```toml
[project.scripts]
kir-pydemo = "kir_pydemo.cli:main"
```

This says: *"Create an executable called `kir-pydemo` that calls the `main()` function in `kir_pydemo.cli`"*

### Step 3: Reinstall the Package

Since we've added a new entry point, we need to reinstall:

```bash
# If you're in editable mode, reinstall to pick up the new entry point
pip install -e .
```

!!! note "Why Reinstall?"
    Entry points are created during installation. Changes to code are reflected immediately in editable mode, but changes to entry points in pyproject.toml require reinstallation.

### Step 4: Test Your CLI

Now test the new command-line interface:

```bash
# Get help
kir-pydemo --help

# Output:
# usage: kir-pydemo [-h] [--version] {gc-content,reverse-complement} ...
# 
# DNA sequence analysis tools
# 
# options:
#   -h, --help            show this help message and exit
#   --version             show program's version number and exit
# 
# commands:
#   {gc-content,reverse-complement}
#                         available commands
#     gc-content          calculate GC content of a DNA sequence
#     reverse-complement  get reverse complement of a DNA sequence
```

```bash
# Calculate GC content
kir-pydemo gc-content ATGCATGC
# Output: GC content: 50.00%

# With custom precision
kir-pydemo gc-content ATGCATGC --precision 1
# Output: GC content: 50.0%

# Reverse complement
kir-pydemo reverse-complement ATGCATGC
# Output: GCATGCAT

# Version
kir-pydemo --version
# Output: kir-pydemo 0.1.0
```

### Step 5: Test File Input

Create a test file with sequences:

```bash
echo -e "ATGCATGC\nAAAAAAAA\nGGGGGGGG" > test_sequences.txt
```

```bash
# Process multiple sequences from file
kir-pydemo gc-content --file test_sequences.txt

# Output:
# GC content: 50.00%
# GC content: 0.00%
# GC content: 100.00%
```

Perfect! Now users can analyze sequences without writing any Python code.

## 🎯 Understanding argparse

Let's break down the key components of our CLI implementation:

### ArgumentParser

```python
parser = argparse.ArgumentParser(
    prog="kir-pydemo",  # Program name shown in help
    description="DNA sequence analysis tools",  # Shown in help
    formatter_class=argparse.RawDescriptionHelpFormatter,  # Preserve formatting
)
```

### Subparsers (Subcommands)

```python
subparsers = parser.add_subparsers(
    title="commands",
    dest="command",  # Stores which subcommand was used in args.command
    required=True,   # Must provide a subcommand
)
```

### Adding Arguments

```python
parser.add_argument(
    "sequence",           # Positional argument (no - or --)
    nargs="?",           # Optional (0 or 1 occurrences)
    help="DNA sequence to analyze",
)

parser.add_argument(
    "-f", "--file",      # Optional argument (short and long form)
    type=Path,           # Convert to Path object
    help="read sequences from file",
)
```

### Argument Types

- **Positional**: `sequence` (no dashes, order matters)
- **Optional**: `-f`, `--file` (dashes, any order)
- **Flags**: `--version`, `-h` (no value needed)

## 📚 Alternative CLI Frameworks

While argparse is in the standard library, there are modern alternatives:

### Click

[Click](https://click.palletsprojects.com/) is a popular framework with a decorator-based syntax:

```python
import click
from kir_pydemo import gc_content

@click.group()
@click.version_option()
def cli():
    """DNA sequence analysis tools."""
    pass

@cli.command()
@click.argument('sequence')
@click.option('-p', '--precision', default=2, help='Decimal precision')
def gc_content_cmd(sequence, precision):
    """Calculate GC content of a DNA sequence."""
    result = gc_content(sequence)
    click.echo(f"GC content: {result:.{precision}f}%")

if __name__ == "__main__":
    cli()
```

**Pros:** Clean syntax, automatic help, rich features
**Cons:** External dependency

### Typer

[Typer](https://typer.tiangolo.com/) builds on Click with type hints:

```python
import typer
from kir_pydemo import gc_content

app = typer.Typer()

@app.command()
def gc_content_cmd(
    sequence: str,
    precision: int = typer.Option(2, help="Decimal precision")
):
    """Calculate GC content of a DNA sequence."""
    result = gc_content(sequence)
    typer.echo(f"GC content: {result:.{precision}f}%")

if __name__ == "__main__":
    app()
```

**Pros:** Type-safe, modern, great IDE support
**Cons:** Requires Python 3.6+, external dependency

!!! tip "Choosing a CLI Framework"
    - **argparse**: Standard library, no dependencies, good for simple CLIs
    - **click**: Feature-rich, mature, great for complex CLIs
    - **typer**: Modern, type-safe, best developer experience
    
    For this tutorial, we use argparse to avoid external dependencies, but feel free to explore others!

## 📋 Checkpoint: What Have We Achieved?

Verify you've successfully completed Episode 2:

- [ ] Created `src/kir_pydemo/cli.py` with CLI implementation
- [ ] Added `[project.scripts]` entry point in `pyproject.toml`
- [ ] Reinstalled the package with `pip install -e .`
- [ ] Successfully run `kir-pydemo gc-content ATGC`
- [ ] Successfully run `kir-pydemo reverse-complement ATGC`
- [ ] Tested file input with `--file` option
- [ ] Checked `kir-pydemo --help` and `kir-pydemo --version`

## 🎯 Key Takeaways

1. **Entry points** create executable commands from Python functions
2. **Console scripts** are defined in `[project.scripts]` in pyproject.toml
3. **argparse** provides powerful command-line parsing (subcommands, options, help)
4. **Good CLIs** return proper exit codes, use stderr for errors, provide help
5. **Reinstallation** is needed after changing entry points

## 🚀 What's Next?

In Episode 3, we'll tackle **Dependencies & Environments**, learning how to:

- Specify package dependencies properly
- Create optional dependencies with "extras"
- Use virtual environments effectively
- Manage dependency conflicts

This is crucial for making your package robust and easy to install!

## 📚 Further Reading

- [argparse tutorial](https://docs.python.org/3/howto/argparse.html)
- [Entry Points Specification](https://packaging.python.org/specifications/entry-points/)
- [Click documentation](https://click.palletsprojects.com/)
- [Typer documentation](https://typer.tiangolo.com/)

---

**Previous:** [← Episode 1: Project Structure](episode-01.md) | **Next:** [Episode 3: Dependencies & Environments →](episode-03.md)
