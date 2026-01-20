# Python Packaging Training - Implementation Guide

## 📦 What's Included

This training repository provides a complete, hands-on guide to modern Python packaging. The materials are designed for learners at BMRC (Kennedy Institute) and beyond who want to transform their Python scripts into professional, distributable packages.

## 🗂️ Repository Structure

```
kir-pydemo-training/
├── docs/                      # MkDocs documentation
│   ├── index.md              # Training home page
│   ├── episode-01.md         # Project structure & pyproject.toml
│   ├── episode-02.md         # Entry points & CLI tools
│   ├── episode-03.md         # Dependencies & environments
│   ├── episode-04.md         # Testing & quality
│   ├── episode-05.md         # Building & distribution
│   └── quick-reference.md    # Quick reference cheat sheet
├── episodes/                  # Working code examples
│   └── episode01/            # Reference implementation for Episode 1
│       ├── src/
│       │   └── kir_pydemo/
│       ├── pyproject.toml
│       └── README.md
├── mkdocs.yml                # MkDocs configuration
└── README.md                 # Repository overview
```

## 🎯 Training Series Overview

### Episode 1: Project Structure & pyproject.toml (45 min)
**What learners build:** A basic installable package
- Modern Python packaging with `pyproject.toml`
- The `src/` layout pattern
- Package metadata and configuration
- Editable installation

### Episode 2: Entry Points & CLI Tools (30 min)
**What learners build:** Command-line tools
- Console scripts and entry points
- Using argparse for CLI
- Subcommand patterns
- User-friendly interfaces

### Episode 3: Dependencies & Environments (40 min)
**What learners build:** Proper dependency management
- Core vs optional dependencies
- Version constraints
- Virtual environments
- Graceful degradation

### Episode 4: Testing & Quality (50 min)
**What learners build:** Tested, quality-controlled package
- pytest for testing
- black/ruff for formatting
- mypy for type checking
- pre-commit hooks

### Episode 5: Building & Distribution (45 min)
**What learners build:** PyPI-ready package
- Building wheels and sdist
- Semantic versioning
- Publishing to PyPI
- GitHub Actions CI/CD

## 🚀 How to Use This Training

### Option 1: Self-Paced Learning

Learners work through episodes independently:

1. **Read the episode documentation** in `docs/episodeXX.md`
2. **Follow along** by creating their own `kir-pydemo` package
3. **Reference example code** in `episodes/episodeXX/` when stuck
4. **Complete checkpoints** to verify understanding

### Option 2: Workshop Format

Instructor-led sessions (3-4 hours total):

**Setup (10 min):**
- Verify Python 3.9+ installed
- Create workspace directory
- Clone/download training materials

**Episode 1 (45 min):**
- Instructor: Live coding demonstration
- Learners: Follow along, create their package
- Q&A and troubleshooting

**Break (10 min)**

**Episode 2 (30 min):**
- Build on previous work
- Add CLI capabilities
- Test the new features

**Episode 3 (40 min):**
- Dependency management discussion
- Add optional dependencies
- Virtual environment best practices

**Break (10 min)**

**Episode 4 (50 min):**
- Quality assurance importance
- Write tests
- Set up linting and formatting

**Episode 5 (45 min):**
- Distribution preparation
- GitHub Actions demo
- Publishing workflow

### Option 3: Documentation Site

Serve as an interactive documentation site:

```bash
# Install MkDocs Material
pip install mkdocs-material

# Serve the documentation
cd kir-pydemo-training
mkdocs serve

# Visit http://127.0.0.1:8000
```

This provides:
- Searchable documentation
- Syntax-highlighted code examples
- Responsive design for mobile/tablet
- Easy navigation between episodes

## 🎓 Learning Objectives

By completing this training, learners will be able to:

- ✅ Structure Python projects using modern best practices
- ✅ Create `pyproject.toml` configurations
- ✅ Build command-line interfaces with entry points
- ✅ Manage dependencies and virtual environments
- ✅ Write comprehensive tests with pytest
- ✅ Implement code quality checks
- ✅ Build and distribute packages to PyPI
- ✅ Set up automated CI/CD pipelines

## 👥 Target Audience

### Primary: BMRC Researchers
- Creating analysis pipelines
- Packaging bioinformatics tools
- Sharing computational methods
- Limited prior packaging experience

### Secondary: General Scientific Python Users
- Any researcher packaging Python code
- Data scientists sharing tools
- Scientists collaborating on software

## 📋 Prerequisites

**Required:**
- Python 3.9 or higher installed
- Basic Python programming knowledge
- Familiarity with command line
- Text editor or IDE

**Helpful but not required:**
- Git/GitHub experience
- Unix shell knowledge
- Prior exposure to pip/virtualenv

## 🔧 Technical Requirements

### Software
- Python 3.9+
- pip (comes with Python)
- Text editor (VS Code, PyCharm, vim, etc.)
- Terminal/command prompt

### Optional (for full experience)
- Git for version control
- GitHub account (for CI/CD episode)
- PyPI/TestPyPI account (for publishing)

## 📝 Customization Notes

### For BMRC Use

The training uses `kir-pydemo` which:
- **kir** = Kennedy Institute of Rheumatology
- **pydemo** = Python demonstration package
- Clearly marks it as educational/demo

### For Other Institutions

Simply search and replace:
- `kir-pydemo` → `your-institution-pydemo`
- "BMRC" → "Your Institution"
- Email addresses and URLs

### For Different Domains

The DNA sequence analysis example can be adapted:
- Physics: Particle data analysis
- Chemistry: Molecular structure tools
- Data Science: Statistical utilities
- General: Text processing or utilities

## 🎯 Key Teaching Points

### Episode 1 Focus
- **Why packaging matters** - Don't just show how, explain why
- **src/ layout benefits** - Emphasize catching installation issues
- **Modern vs legacy** - Show evolution from setup.py

### Episode 2 Focus
- **User experience** - Good CLIs are discoverable and helpful
- **Subcommands pattern** - Used by git, docker, many tools
- **argparse depth** - Standard library, no dependencies

### Episode 3 Focus
- **Dependency philosophy** - Core vs optional, constraints
- **Virtual environments** - Why they're essential
- **Graceful degradation** - Handle missing optional deps well

### Episode 4 Focus
- **Test-driven mindset** - Write tests as you code
- **Automation wins** - Pre-commit prevents issues
- **Coverage metrics** - Useful but not the only goal

### Episode 5 Focus
- **Versioning strategy** - Semantic versioning explained
- **CI/CD value** - Automation prevents mistakes
- **Documentation importance** - Good docs = adoption

## 💡 Teaching Tips

### Common Questions

**Q: "Should I use poetry instead of setuptools?"**
A: Poetry is great, but setuptools is more universal. This training teaches fundamentals that apply to any tool.

**Q: "Do I really need the src/ layout?"**
A: It's a best practice that prevents subtle bugs. For serious packages, yes.

**Q: "When should I publish to PyPI?"**
A: When the package provides value to others and you're committed to maintaining it.

### Common Issues

1. **Import errors after installing**
   - Usually missing `__init__.py` or wrong directory structure
   - Solution: Check src/ layout carefully

2. **Entry point not found**
   - Forgot to reinstall after changing pyproject.toml
   - Solution: `pip install -e .` again

3. **Tests not discovered**
   - Wrong naming (must be `test_*.py`)
   - Solution: Follow pytest conventions

4. **Virtual environment confusion**
   - Installed in system instead of venv
   - Solution: Always activate venv first

## 📈 Assessment Ideas

### Checkpoints (in each episode)
Self-assessment questions and tasks

### Mini-Project
Package a simple tool of their own choice

### Code Review Exercise
Review a peer's package structure

### Presentation
Present their package to the group

## 🔄 Maintenance and Updates

### Regular Updates Needed
- Python version support
- Dependency versions
- Tool versions (black, ruff, mypy)
- GitHub Actions versions

### Semi-Regular Updates
- Best practices evolution
- New packaging standards (PEPs)
- Tool recommendations

### Rarely Change
- Core concepts (pyproject.toml, src/ layout)
- Semantic versioning principles
- Testing fundamentals

## 📚 Additional Resources

### Provided in Training
- Quick reference guide
- Complete working examples
- Comprehensive documentation

### External Resources (mentioned in docs)
- Python Packaging User Guide
- PyPI documentation
- Tool-specific docs (pytest, black, etc.)

## 🎁 Bonus Content Ideas

Future additions could include:

- **Episode 6: Advanced Topics**
  - Binary extensions with C/Cython
  - Conda packaging
  - Cross-platform considerations

- **Episode 7: Documentation Deep Dive**
  - Sphinx comprehensive guide
  - API documentation generation
  - Docstring standards

- **Episode 8: Community Standards**
  - Contributing guidelines
  - Code of conduct
  - Issue templates

## ✅ Training Delivery Checklist

**Before the training:**
- [ ] Test all code examples
- [ ] Verify links work
- [ ] Check all commands on target platform
- [ ] Prepare backup materials (no internet scenarios)
- [ ] Test MkDocs site rendering

**During the training:**
- [ ] Provide pre-built examples for reference
- [ ] Have troubleshooting resources ready
- [ ] Take notes on common issues
- [ ] Gather feedback

**After the training:**
- [ ] Collect feedback
- [ ] Update materials based on issues encountered
- [ ] Provide follow-up resources
- [ ] Track learner progress

## 🤝 Contribution and Improvement

This training is designed to evolve. Suggested improvements:

- Add more domain-specific examples
- Include advanced topics
- Create video walkthroughs
- Add interactive exercises
- Develop automated assessment tools

## 📞 Support and Questions

For BMRC-specific support:
- Contact the training organizer
- Post in internal channels
- Reference this documentation

For general Python packaging questions:
- Python Packaging User Guide
- Stack Overflow (tag: python-packaging)
- Python Discourse

---

**Ready to start?** See [README.md](README.md) for getting started instructions!

**Questions about implementation?** This guide should help instructors and self-learners make the most of the materials.
