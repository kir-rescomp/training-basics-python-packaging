# Supplementary: Making Your CLI Beautiful

!!! note-sticky "Supplementary Material"
    This is bonus content that builds on **Episode 2: Entry Points & CLI Tools**. It shows how to add colors, tables, and formatted output to your command-line interface.

## 🎨 Why Beautiful CLIs Matter

Compare these two outputs:

**Plain:**
<div class="nord" markdown="1">
```py
Processing file1.txt
Processing file2.txt
Error: file3.txt not found
Done. Processed 2 files.
```


**Enhanced:**
```rust
✓ Processing file1.txt
✓ Processing file2.txt
✗ Error: file3.txt not found
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Done. Processed 2 files.
```
</div>

The enhanced version is:
- **Easier to scan** - symbols and colors help spot issues quickly
- **More professional** - looks polished and well-maintained
- **User-friendly** - clear visual hierarchy

## 📦 The `rich` Library

[`rich`](https://rich.readthedocs.io/) is a Python library for rich text and beautiful formatting in the terminal.

**Features:**

- ✅ Cross-platform color support (Windows, Mac, Linux)
- ✅ Tables, progress bars, syntax highlighting
- ✅ Panels, columns, and layout
- ✅ Automatic detection of terminal capabilities

**Installation:**
```bash
pip install rich
```

## 🔧 Adding Rich to kir-pydemo

### Step 1: Make It an Optional Dependency

Edit `pyproject.toml`:

```toml
[project.optional-dependencies]
bio = ["biopython>=1.80"]
plotting = ["matplotlib>=3.5.0", "numpy>=1.20.0"]
cli-extras = ["rich>=13.0.0"]  # ← New!
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
]
```

Now users can install it with:
```bash
pip install kir-pydemo[cli-extras]
```

### Step 2: Implement Graceful Degradation

The CLI should work **with or without** rich installed.

**Pattern:**
```python
# At the top of cli.py
try:
    from rich.console import Console
    from rich.panel import Panel
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

# Then use conditional logic
def print_success(message: str):
    """Print success message with color if available."""
    if HAS_RICH:
        console.print(f"[green]✓[/green] {message}")
    else:
        print(f"✓ {message}")
```

This way:
- ✅ Works great with `rich` installed
- ✅ Still works fine without it (plain text)
- ✅ No crashes or ImportErrors

## 🎯 Practical Examples

### Example 1: Colored Output

**Update `cli.py` with helper functions:**

```python
"""Command-line interface for kir-pydemo."""

import argparse
import sys
from pathlib import Path

from kir_pydemo import gc_content, reverse_complement, __version__

# Try to import rich
try:
    from rich.console import Console
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None


def print_success(message: str):
    """Print success message."""
    if HAS_RICH:
        console.print(f"[green]✓[/green] {message}")
    else:
        print(f"✓ {message}")


def print_error(message: str):
    """Print error message."""
    if HAS_RICH:
        console.print(f"[red]✗[/red] {message}", file=sys.stderr)
    else:
        print(f"✗ {message}", file=sys.stderr)


def print_result(label: str, value: str, highlight: bool = False):
    """Print a result value."""
    if HAS_RICH:
        if highlight:
            console.print(f"{label}: [bold green]{value}[/bold green]")
        else:
            console.print(f"{label}: {value}")
    else:
        print(f"{label}: {value}")
```

**Use in your commands:**

```python
def cmd_gc_content(args: argparse.Namespace) -> int:
    """Handle the gc-content command."""
    # ... existing code to get sequences ...
    
    try:
        result = gc_content(sequence)
        print_result("GC content", f"{result:.{args.precision}f}%", highlight=True)
        return 0
    except ValueError as e:
        print_error(str(e))
        return 1
```

### Example 2: Banner

Add a colorful banner:

```python
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich import box
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None


def print_banner():
    """Print a colorful banner."""
    if HAS_RICH:
        banner_text = f"""
[bold cyan]kir-pydemo[/bold cyan] v{__version__}
[dim]DNA Sequence Analysis Tools[/dim]

[yellow]Features:[/yellow]
  • GC content calculation
  • Reverse complement generation
  • FASTA file support
        """
        console.print(Panel(
            banner_text,
            box=box.ROUNDED,
            border_style="cyan",
            padding=(1, 2)
        ))
    else:
        # Plain fallback
        print(f"\nkir-pydemo v{__version__}")
        print("DNA Sequence Analysis Tools\n")


# Add --banner flag to parser
parser.add_argument(
    "--banner",
    action="store_true",
    help="Show banner (requires rich)",
)

# In main()
def main() -> int:
    parser = create_parser()
    args = parser.parse_args()
    
    if args.banner:
        print_banner()
    
    # ... rest of main
```

**Usage:**
```bash
kir-pydemo --banner gc-content ATGC
```

**Output (with rich):**
```
╭─────────────────────────────────────╮
│                                     │
│  kir-pydemo v0.1.0                  │
│  DNA Sequence Analysis Tools        │
│                                     │
│  Features:                          │
│    • GC content calculation         │
│    • Reverse complement generation  │
│    • FASTA file support             │
│                                     │
╰─────────────────────────────────────╯
```

### Example 3: Tables for Multiple Results

When processing multiple sequences:

```python
try:
    from rich.console import Console
    from rich.table import Table
    from rich import box
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None


def print_results_table(results: list):
    """Print results in a table format."""
    if HAS_RICH:
        table = Table(title="GC Content Analysis", box=box.SIMPLE)
        table.add_column("Sequence", style="cyan", no_wrap=False)
        table.add_column("GC %", justify="right", style="green")
        
        for seq, gc_val in results:
            # Truncate long sequences
            display_seq = seq[:30] + "..." if len(seq) > 30 else seq
            
            # Color-code based on GC content
            if gc_val < 40:
                gc_style = "blue"
            elif gc_val > 60:
                gc_style = "red"
            else:
                gc_style = "green"
            
            table.add_row(
                display_seq,
                f"[{gc_style}]{gc_val:.2f}[/{gc_style}]"
            )
        
        console.print(table)
    else:
        # Plain text fallback
        print("\nGC Content Analysis")
        print("-" * 50)
        for seq, gc_val in results:
            display_seq = seq[:30] + "..." if len(seq) > 30 else seq
            print(f"{display_seq:35} {gc_val:6.2f}%")
        print("-" * 50)
```

**Add table option to parser:**

```python
gc_parser.add_argument(
    "-t", "--table",
    action="store_true",
    help="Display results in table format",
)
```

**Usage:**
```bash
kir-pydemo gc-content --file sequences.txt --table
```

**Output (with rich):**
```
      GC Content Analysis      
┌────────────────────────┬────────┐
│ Sequence               │  GC %  │
├────────────────────────┼────────┤
│ ATGCATGC               │  50.00 │
│ AAAAAAAAAA             │   0.00 │
│ GGGGGGGGGG             │ 100.00 │
└────────────────────────┴────────┘
```

### Example 4: Progress Bar (Bonus)

For long-running operations:

```python
from rich.progress import track

def process_fasta_file(filepath: Path):
    """Process FASTA file with progress bar."""
    sequences = read_fasta(filepath)
    
    if HAS_RICH:
        results = []
        for name, seq in track(sequences, description="Processing..."):
            gc_val = gc_content(seq)
            results.append((name, seq, gc_val))
        return results
    else:
        # Plain version
        results = []
        for name, seq in sequences:
            gc_val = gc_content(seq)
            results.append((name, seq, gc_val))
            print(f"Processed {name}")
        return results
```

## 🎨 Rich Color Reference

**Common color names:**
- `red`, `green`, `blue`, `yellow`, `cyan`, `magenta`
- `bright_red`, `bright_green`, etc.

**Text styles:**
- `[bold]text[/bold]` - Bold
- `[dim]text[/dim]` - Dimmed
- `[italic]text[/italic]` - Italic
- `[underline]text[/underline]` - Underlined

**Combinations:**
```python
console.print("[bold red]Error![/bold red]")
console.print("[green]✓[/green] [dim]Success[/dim]")
```

## 📋 Best Practices

### 1. Always Provide Fallbacks

```python
# ✅ Good - works with or without rich
if HAS_RICH:
    console.print("[green]Success[/green]")
else:
    print("Success")

# ❌ Bad - crashes without rich
console.print("[green]Success[/green]")  # NameError if not installed
```

### 2. Don't Overuse Colors

```python
# ✅ Good - colors have meaning
print_error("File not found")  # Red
print_success("Done!")         # Green

# ❌ Bad - rainbow soup
console.print("[red]The[/red] [blue]quick[/blue] [green]brown[/green]...")
```

### 3. Respect NO_COLOR Environment Variable

Rich automatically respects the `NO_COLOR` environment variable. Users can disable colors:

```bash
NO_COLOR=1 kir-pydemo gc-content ATGC
```

### 4. Test Without Rich

Always test that your CLI works without rich installed:

```bash
# Create a test environment without rich
python -m venv test-env
source test-env/bin/activate
pip install -e .  # Without [cli-extras]

# Should still work, just without colors
kir-pydemo gc-content ATGC
```

## 🚀 Real-World Examples

Other popular tools using rich:

- **Poetry** - Python dependency management
- **Typer** - CLI framework (built on rich)
- **HTTPie** - HTTP client
- **Pre-commit** - Git hooks framework

## 📚 Further Reading

- [Rich Documentation](https://rich.readthedocs.io/)
- [Rich Gallery](https://rich.readthedocs.io/en/stable/introduction.html#quick-start) - Examples
- [Typer](https://typer.tiangolo.com/) - CLI framework with rich integration
- [Click Rich](https://github.com/ewels/rich-click) - Rich formatting for Click

## ✅ Summary

Adding rich to your CLI:

1. **Add as optional dependency** - `[project.optional-dependencies]`
2. **Check if available** - `try/except ImportError`
3. **Provide fallbacks** - Plain text when rich isn't installed
4. **Use colors meaningfully** - Red for errors, green for success
5. **Keep it simple** - Don't overdo it

**Remember:** A CLI should work perfectly without rich - colors are a nice enhancement, not a requirement!

---

**Back to:** [Episode 2: Entry Points & CLI Tools](episode-02.md)
