# Python Packaging Basics: A Practical Guide

Welcome to the **Python Packaging Basics** training series! This repository provides a hands-on, story-driven approach to learning modern Python packaging.

## 🎯 What You'll Learn

Through building `kir-pydemo`, a simple bioinformatics utility package, you'll master:

- Modern Python packaging with `pyproject.toml`
- The `src/` layout pattern
- Creating installable packages
- Building CLI tools with entry points
- Managing dependencies
- Testing and code quality
- Building and distributing packages

## 📚 Episodes

This training is divided into five progressive episodes, each building on the previous:

1. **[Episode 1: Project Structure & pyproject.toml](docs/episode-01.md)**
   - Introduction to modern Python packaging
   - Setting up project structure with `src/` layout
   - Creating your first `pyproject.toml`
   - Making your package installable

2. **[Episode 2: Entry Points & CLI Tools](docs/episode-02.md)**
   - Adding command-line interfaces
   - Console scripts and entry points
   - Argument parsing basics

3. **[Episode 3: Dependencies & Environments](docs/episode-03.md)**
   - Managing dependencies properly
   - Optional dependencies for extras
   - Virtual environments best practices

4. **[Episode 4: Testing & Quality](docs/episode-04.md)**
   - Adding tests with pytest
   - Code quality tools (ruff, black, mypy)
   - Pre-commit hooks

5. **[Episode 5: Building & Distribution](docs/episode-05.md)**
   - Building wheels and source distributions
   - Version management strategies
   - Publishing to PyPI or private repositories

## 🚀 Getting Started

Each episode has:
- **Concept explanations** - Clear, concise theory
- **Working code examples** - In the `episodes/` directory
- **Step-by-step instructions** - Follow along and build
- **Checkpoints** - Verify your understanding
- **Best practices** - Learn the right way

### Prerequisites

- Python 3.9 or higher
- Basic Python programming knowledge
- Familiarity with command line

### How to Use This Repository

1. **Read the episode documentation** in the `docs/` folder
2. **Follow along** by creating your own version of `kir-pydemo`
3. **Reference the example code** in `episodes/episodeXX/` for comparison
4. **Complete the checkpoints** to verify your progress

## 📖 Documentation Site

You can browse this as a documentation site using MkDocs:

```bash
pip install mkdocs-material
mkdocs serve
```

Then visit http://127.0.0.1:8000

## 🎓 Who Is This For?

This training is designed for:
- Researchers packaging their analysis tools
- Scientists sharing computational methods
- Anyone wanting to understand modern Python packaging
- Developers moving from scripts to packages

## 📝 License

This training material is provided for educational purposes.

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to open an issue or submit a pull request!

---

**Ready to begin?** Start with [Episode 1: Project Structure & pyproject.toml](docs/episode-01.md)
