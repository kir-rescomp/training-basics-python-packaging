# Python Packaging Basics: A Practical Guide

Welcome to **Python Packaging Basics**! This training series will teach you how to create professional, installable Python packages using modern best practices.

## 🎯 What You'll Build

Throughout this series, you'll build **kir-pydemo**, a simple but complete bioinformatics package for DNA sequence analysis. By the end, you'll have a package that:

- ✅ Can be installed with `pip install kir-pydemo`
- ✅ Has command-line tools: `kir-pydemo gc-content ATGC`
- ✅ Manages dependencies properly
- ✅ Includes tests and quality checks
- ✅ Can be published to PyPI

## 📚 The Episodes

### [Episode 1: Project Structure & pyproject.toml](episode-01.md)

**Duration:** ~45 minutes

Learn the foundation of modern Python packaging:

- Understanding pyproject.toml vs setup.py
- The src/ layout pattern
- Package metadata and configuration
- Installing in editable mode

**You'll create:** A basic installable package

---

### [Episode 2: Entry Points & CLI Tools](episode-02.md)

**Duration:** ~30 minutes

Make your package executable from the command line:

- Console scripts and entry points
- Command-line argument parsing
- Building user-friendly CLIs

**You'll create:** Command-line tools for sequence analysis

---

### [Episode 3: Dependencies & Environments](episode-03.md)

**Duration:** ~40 minutes

Master dependency management:

- Specifying dependencies in pyproject.toml
- Optional dependencies and extras
- Virtual environments best practices
- Lock files and reproducibility

**You'll create:** A properly managed dependency structure

---

### [Episode 4: Testing & Quality](episode-04.md)

**Duration:** ~50 minutes

Ensure code quality and reliability:

- Adding tests with pytest
- Code formatting with black/ruff
- Type checking with mypy
- Pre-commit hooks for automation

**You'll create:** A tested, quality-controlled package

---

### [Episode 5: Building & Distribution](episode-05.md)

**Duration:** ~45 minutes

Share your package with the world:

- Building wheels and source distributions
- Version management strategies
- Publishing to PyPI
- Documentation with Sphinx

**You'll create:** A distributable package ready for PyPI

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** installed
- Basic Python programming knowledge
- Familiarity with the command line
- A text editor or IDE

### Recommended Setup

```bash
# Check your Python version
python --version  # Should be 3.9 or higher

# Create a workspace for the training
mkdir python-packaging-training
cd python-packaging-training

# Clone or download this repository
git clone <repository-url>
cd kir-pydemo-training
```

### How to Use This Material

1. **Read each episode sequentially** - They build on each other
2. **Follow along by coding** - Don't just read, do!
3. **Check the examples** - Reference code is in `episodes/episodeXX/`
4. **Complete the checkpoints** - Verify your understanding
5. **Experiment** - Try modifications and see what happens

## 💡 Learning Approach

This training uses a **story-driven approach**:

- Each episode continues the story of building kir-pydemo
- Concepts are introduced when needed, not all at once
- Real-world examples and problems
- Progressive complexity

## 🎓 Who Is This For?

This training is designed for:

- **Researchers** packaging analysis tools
- **Scientists** sharing computational methods
- **Developers** learning Python packaging
- **Anyone** moving from scripts to packages

You should know basic Python, but you don't need prior packaging experience.



## 🤔 Getting Help

If you encounter issues:

1. Check the checkpoint sections in each episode
2. Compare your code with the examples in `episodes/episodeXX/`
3. Review the "Common Issues" sections
4. Consult the [Quick Reference](quick-reference.md) guide

## 📝 Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI - Python Package Index](https://pypi.org/)
- [setuptools documentation](https://setuptools.pypa.io/)
- [PEP 517 - Build System Interface](https://peps.python.org/pep-0517/)
- [PEP 518 - pyproject.toml specification](https://peps.python.org/pep-0518/)

---

**Ready to begin?** Start with [Episode 1: Project Structure & pyproject.toml →](episode-01.md)
