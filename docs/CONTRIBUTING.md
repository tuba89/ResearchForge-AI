# Contributing to ResearchForge AI

Thank you for your interest in contributing to ResearchForge AI! We welcome contributions from everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)

---

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards others

**Unacceptable behavior includes:**
- Harassment, trolling, or discriminatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

---

## 🛠️ How Can I Contribute?

### Reporting Bugs

Found a bug? Please create an issue with:

**Required Information:**
- **Clear title** (e.g., "Search fails for queries with special characters")
- **Description** of what happened vs. what you expected
- **Steps to reproduce:**
  ```
  1. Go to search page
  2. Enter query with "&" symbol
  3. Click search
  4. See error
  ```
- **Screenshots** if applicable
- **Environment:**
  - OS: (e.g., macOS 14.0)
  - Browser: (e.g., Chrome 120)
  - Python: (e.g., 3.12.0)

**Label your issue:** `bug`

### Suggesting Features

We love new ideas! Before suggesting:

1. **Check existing issues** to avoid duplicates
2. **Create an issue** with `enhancement` label
3. **Include:**
   - Clear description of the feature
   - Why it would be useful
   - How it should work (with examples)
   - Any potential drawbacks

**Example:**
```markdown
Title: Add export to PDF feature for proposals

Description:
Allow users to export generated research proposals as PDF files.

Benefits:
- Easier sharing with collaborators
- Professional formatting
- Offline access

Implementation ideas:
- Add "Export PDF" button in proposal view
- Use WeasyPrint or similar library
- Maintain formatting and styling
```

### Improving Documentation

Documentation improvements are always welcome:

- Fix typos or unclear explanations
- Add examples or tutorials
- Improve API documentation
- Translate to other languages

### Contributing Code

See [Pull Request Process](#pull-request-process) below.

---

## 💻 Development Setup

### Prerequisites

- Python 3.12+
- Git
- Google API key ([Get one](https://aistudio.google.com/apikey))

### Setup Steps

1. **Fork the repository**
   
   Click "Fork" button on GitHub

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/ResearchForge-AI.git
   cd ResearchForge-AI
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/ResearchForge-AI.git
   ```

4. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Dev dependencies
   ```

6. **Set up environment**
   ```bash
   cp .env.template .env
   # Edit .env with your API key
   ```

7. **Run the app**
   ```bash
   python app.py
   ```

8. **Run tests**
   ```bash
   pytest tests/
   ```

---

## 📝 Code Style Guidelines

### Python

**Follow PEP 8:**
- 4 spaces for indentation
- Max line length: 100 characters
- Use meaningful variable names

**Type hints:**
```python
def search_papers(query: str, max_results: int = 10) -> Dict[str, Any]:
    """Search for papers."""
    pass
```

**Docstrings:**
```python
def advanced_arxiv_search(query: str, category: str = "all") -> Dict[str, Any]:
    """
    Search arXiv for research papers.
    
    Args:
        query: Search query string
        category: arXiv category filter (e.g., 'cs.AI')
        
    Returns:
        Dictionary with status and papers list
        
    Raises:
        ValueError: If query is empty
    """
    pass
```

**Use Black formatter:**
```bash
pip install black
black app.py
```

### JavaScript

**ES6+ features:**
```javascript
// Good
const searchPapers = async (query) => {
    const response = await fetch('/api/search', {
        method: 'POST',
        body: JSON.stringify({ query })
    });
    return response.json();
};

// Avoid
function searchPapers(query) {
    return fetch('/api/search', {
        method: 'POST',
        body: JSON.stringify({ query: query })
    }).then(function(response) {
        return response.json();
    });
}
```

**Error handling:**
```javascript
try {
    const data = await searchPapers(query);
    displayResults(data);
} catch (error) {
    console.error('Search failed:', error);
    showErrorMessage(error.message);
}
```

### HTML/CSS

**Semantic HTML:**
```html
<!-- Good -->
<nav>
    <ul>
        <li><a href="#features">Features</a></li>
    </ul>
</nav>

<!-- Avoid -->
<div class="nav">
    <div class="nav-item">
        <div onclick="goto('#features')">Features</div>
    </div>
</div>
```

**TailwindCSS:**
```html
<!-- Use utility classes -->
<button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
    Search
</button>
```

**Accessibility:**
```html
<button aria-label="Search papers">
    <i class="fas fa-search"></i>
</button>
```

---

## 💬 Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/).

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

**Good:**
```
feat(search): add category filter for arXiv search

- Added dropdown for category selection
- Updated API to accept category parameter
- Added tests for category filtering

Closes #42
```

```
fix(chat): resolve markdown rendering issue

The markdown parser was not handling code blocks correctly.
Updated to use marked.js library for proper parsing.

Fixes #38
```

**Bad:**
```
Updated stuff
```

```
Fixed bug
```

### Tips

- Use present tense ("add" not "added")
- Keep subject under 50 characters
- Reference issues and PRs in footer

---

## 🔀 Pull Request Process

### Before Submitting

1. **Sync with upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make changes**
   - Write code
   - Add tests
   - Update documentation

4. **Test locally**
   ```bash
   # Run tests
   pytest tests/
   
   # Check code style
   black --check app.py
   flake8 app.py
   
   # Test the app
   python app.py
   ```

5. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

### Creating the Pull Request

1. **Go to GitHub** and click "New Pull Request"

2. **Fill out the template:**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [x] New feature
   - [ ] Documentation update
   
   ## Testing
   - [x] I have tested these changes locally
   - [x] I have added tests for new functionality
   - [x] All tests pass
   
   ## Checklist
   - [x] Code follows style guidelines
   - [x] Documentation updated
   - [x] No breaking changes
   
   ## Related Issues
   Closes #42
   ```

3. **Request review** from maintainers

### Review Process

Maintainers will:
1. Review code for quality and style
2. Test functionality
3. Provide feedback or approve
4. Merge when approved

**Be patient!** Reviews may take 1-3 days.

### After Approval

Once merged:
1. Delete your feature branch
2. Sync your fork with upstream
3. Celebrate! 🎉

---

## 🧪 Testing

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_search.py

# With coverage
pytest --cov=app tests/
```

### Writing Tests

**Example test:**
```python
def test_arxiv_search():
    """Test arXiv search functionality."""
    result = advanced_arxiv_search("machine learning", max_results=5)
    
    assert result["status"] == "success"
    assert len(result["papers"]) <= 5
    assert all("title" in paper for paper in result["papers"])
```

---

## 📚 Documentation

### Code Comments

**Good:**
```python
# Calculate similarity using cosine distance
similarity = 1 - cosine(vec1, vec2)
```

**Unnecessary:**
```python
# Increment i by 1
i += 1
```

### Updating Docs

When you add features:
- Update README.md
- Update API documentation
- Add usage examples
- Update DEPLOY.md if needed

---

## 🎯 Project Priorities

**High Priority:**
- Bug fixes
- Performance improvements
- Security updates
- Critical features

**Medium Priority:**
- New features
- UI/UX improvements
- Test coverage

**Low Priority:**
- Code cleanup
- Documentation
- Nice-to-have features

---

## ❓ Questions?

- **General questions:** Open a [Discussion](https://github.com/yourusername/ResearchForge-AI/discussions)
- **Bugs:** Open an [Issue](https://github.com/yourusername/ResearchForge-AI/issues)
- **Security:** Email security@yourdomain.com

---

## 🙏 Recognition

Contributors will be:
- Added to README.md
- Mentioned in release notes
- Forever appreciated! ❤️

---

<div align="center">

**Thank you for contributing to ResearchForge AI!** 🚀

Made with ❤️ by the community

</div>
