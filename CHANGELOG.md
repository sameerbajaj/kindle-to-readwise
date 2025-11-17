# Changelog

All notable changes to the Kindle to Readwise Converter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-15

### Added
- Initial release of Kindle to Readwise Converter
- HTML parser for Kindle Notebook exports
- CSV export in Readwise-compatible format
- Google Books API integration for metadata fetching
- Automatic chapter heading detection and `.h1` formatting
- Pink highlight detection and `.favorite` tagging
- Note attachment to corresponding highlights
- Intelligent page number backfilling
- Interactive CLI mode with user prompts
- Command-line argument support
- Three usage modes (interactive, CLI, Python module)
- Comprehensive error handling
- Example HTML file for testing
- Cross-platform support (Mac, Windows, Linux)

### Documentation
- Comprehensive README with installation and usage
- Quick Start guide for 2-minute setup
- Detailed Usage guide with examples
- Visual Workflow documentation
- Contributing guidelines
- MIT License
- Example HTML file
- Setup script for automated installation

### Technical
- Python 3.7+ support
- Dependencies: pandas, beautifulsoup4, requests, lxml
- Modular function architecture
- Type hints and docstrings
- Clean code with PEP 8 compliance
- GitHub Actions workflow for automated testing

## [Unreleased]

### Planned Features
- Batch processing for multiple HTML files
- GUI version for non-technical users
- Support for Kobo and Apple Books formats
- Direct Readwise API integration
- Progress bars for large files
- Export statistics and summary
- Deduplication of highlights
- Configurable output format
- Dark mode for GUI
- Mobile app version
- Browser extension

### Known Issues
- None currently reported

## How to Report Issues

If you encounter any problems:
1. Check the [Troubleshooting section](README.md#troubleshooting)
2. Search [existing issues](https://github.com/sameerbajaj/kindle-to-readwise/issues)
3. [Open a new issue](https://github.com/sameerbajaj/kindle-to-readwise/issues/new) with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)
   - Sample file (if possible)

## Release Notes

### v1.0.0 - Initial Release

This is the first stable release of the Kindle to Readwise Converter. The tool has been tested with various Kindle exports and successfully imports highlights to Readwise with proper formatting.

**Key Features:**
- 📚 Converts Kindle HTML exports to Readwise CSV
- 🎯 Proper chapter headings (`.h1` tags)
- 💖 Pink highlights marked as favorites
- 📝 Notes attached to their highlights
- 📍 Missing page numbers intelligently filled
- 🌐 Book metadata from Google Books API
- 🚀 Easy to use with multiple interfaces
- 📖 Comprehensive documentation

**What's Working:**
- ✅ All Kindle Notebook HTML exports
- ✅ Yellow and pink highlights
- ✅ Notes and annotations
- ✅ Chapter/section headings
- ✅ Page and location numbers
- ✅ Multi-author books
- ✅ Books without ISBN
- ✅ Large files (500+ highlights)

**Tested On:**
- macOS 12+ (Intel and Apple Silicon)
- Windows 10/11
- Ubuntu 20.04+
- Python 3.7, 3.8, 3.9, 3.10, 3.11

---

For the full history, see the [commit log](https://github.com/sameerbajaj/kindle-to-readwise/commits/main).
