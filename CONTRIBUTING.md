# Contributing to Enterprise RAG

Thank you for your interest in contributing to Enterprise RAG! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to riteshrana36@gmail.com.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce the behavior
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, Python version, package versions
- **Logs**: Relevant log output or error messages

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use Case**: Why this enhancement would be useful
- **Proposed Solution**: How you envision it working
- **Alternatives**: Alternative solutions you've considered
- **Impact**: Expected impact on performance, usability, or complexity

### Contributing Code

We welcome production-tested patterns and improvements! Here's how to contribute:

#### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/your-username/Enterprise-Rag.git
cd Enterprise-Rag
```

#### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

#### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

#### 4. Make Your Changes

Follow these guidelines:

- **Code Style**: Follow PEP 8, use Black for formatting
- **Type Hints**: Add type hints to all functions
- **Docstrings**: Use Google-style docstrings
- **Tests**: Add tests for new functionality
- **Documentation**: Update relevant documentation

#### 5. Run Tests and Linting

```bash
# Format code
black src/ tests/

# Check linting
ruff check src/ tests/

# Type checking
mypy src/

# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

#### 6. Commit Your Changes

Write clear, concise commit messages:

```bash
git add .
git commit -m "feat: add hybrid search optimization

- Implement dynamic weight adjustment based on query type
- Add caching for BM25 index
- Update tests and documentation"
```

Commit message format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `chore:` Maintenance tasks

#### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- **Title**: Clear, descriptive title
- **Description**: What changes were made and why
- **Testing**: How you tested the changes
- **Screenshots**: If applicable (UI changes)
- **Breaking Changes**: Note any breaking changes
- **Related Issues**: Link to related issues

## Development Guidelines

### Code Style

```python
# Good: Type hints, docstring, clear naming
from typing import List, Optional
from pydantic import BaseModel

def process_documents(
    documents: List[str],
    chunk_size: int = 512,
    overlap: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Process documents into chunks.
    
    Args:
        documents: List of document texts to process
        chunk_size: Size of chunks in tokens
        overlap: Overlap between chunks in tokens
        
    Returns:
        List of processed chunks with metadata
        
    Raises:
        ValueError: If chunk_size is invalid
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    
    # Implementation
    pass
```

### Testing

Write tests for all new functionality:

```python
# tests/unit/test_chunking.py
import pytest
from src.document_processing.chunking import HierarchicalChunker

class TestHierarchicalChunker:
    def test_basic_chunking(self):
        """Test basic chunking functionality."""
        chunker = HierarchicalChunker(chunk_size=100)
        text = "Sample text " * 50
        
        chunks = chunker.chunk(text)
        
        assert len(chunks) > 0
        assert all(len(chunk) <= 100 for chunk in chunks)
    
    def test_respects_sections(self):
        """Test that section boundaries are respected."""
        chunker = HierarchicalChunker(respect_sections=True)
        text = "# Section 1\nContent\n\n# Section 2\nMore content"
        
        chunks = chunker.chunk(text)
        
        # Verify sections are not split
        assert "# Section 1" in chunks[0]
        assert "# Section 2" not in chunks[0]
```

### Documentation

Update documentation for:
- New features or changes to existing features
- New configuration options
- API changes
- Deployment changes

### Production-Tested Patterns

We prioritize contributions that:
- Have been tested in real deployments
- Include performance benchmarks
- Address common pain points
- Maintain backward compatibility
- Include comprehensive tests

## Pull Request Review Process

1. **Automated Checks**: CI/CD runs tests, linting, type checking
2. **Code Review**: Maintainers review code quality and design
3. **Testing**: Verify functionality works as expected
4. **Documentation**: Ensure documentation is updated
5. **Approval**: At least one maintainer approval required
6. **Merge**: Squash and merge to main branch

## Community

- **GitHub Discussions**: Ask questions, share ideas
- **Issues**: Report bugs, request features
- **Email**: riteshrana36@gmail.com for private inquiries

## Recognition

Contributors are recognized in:
- README.md (Contributors section)
- Release notes
- GitHub contributors page

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing, please:
1. Check existing documentation
2. Search GitHub issues and discussions
3. Create a new discussion
4. Email riteshrana36@gmail.com

Thank you for contributing to Enterprise RAG!
