# Contributing to Kindle to Readwise Converter

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior vs actual behavior
- Your environment (Python version, OS)
- Sample HTML file (if possible) or description of the structure

### Suggesting Enhancements

We welcome feature requests! Please create an issue with:
- A clear description of the feature
- Why this feature would be useful
- Examples of how it would work

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes**
   - Write clear, commented code
   - Follow PEP 8 style guidelines
   - Add docstrings to functions
   - Update README.md if needed

3. **Test your changes**
   ```bash
   python kindle_to_readwise.py example.html
   ```

4. **Commit your changes**
   ```bash
   git commit -m "Add feature: description of feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/my-new-feature
   ```

6. **Open a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Explain how you tested the changes

## Development Setup

```bash
# Clone your fork
git clone https://github.com/sameerbajaj/kindle-to-readwise.git
cd kindle-to-readwise

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the example
python kindle_to_readwise.py example.html
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Write docstrings for functions
- Keep functions focused and single-purpose

## Testing

Currently, testing is manual. Run the script with the example HTML file:

```bash
python kindle_to_readwise.py example.html
```

Verify that:
- ✅ CSV is created successfully
- ✅ Chapter headings have `.h1` tags
- ✅ Pink highlights have `.favorite` tags
- ✅ Notes are attached to highlights
- ✅ Page numbers are filled correctly

## Areas for Improvement

Want to contribute but not sure where to start? Here are some ideas:

### High Priority
- [ ] Automated unit tests
- [ ] Batch processing for multiple files
- [ ] Better error messages with recovery suggestions
- [ ] Progress bar for large files

### Medium Priority
- [ ] GUI version (tkinter or PyQt)
- [ ] Support for Kobo exports
- [ ] Support for Apple Books exports
- [ ] Option to deduplicate highlights
- [ ] Configurable output format

### Nice to Have
- [ ] Web-based version
- [ ] Docker container
- [ ] Integration with Readwise API (direct upload)
- [ ] Export statistics and summary
- [ ] Dark mode for GUI version

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
