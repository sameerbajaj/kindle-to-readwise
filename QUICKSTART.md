# Quick Start Guide

Get started in 2 minutes! ⚡

## 1. Install Dependencies

### Mac/Linux:
```bash
./setup.sh
```

### Windows:
```bash
pip install -r requirements.txt
```

### Manual:
```bash
pip3 install pandas beautifulsoup4 requests lxml
```

## 2. Export from Kindle

1. Open Kindle app
2. Press `Cmd+Shift+N` (Mac) or `Ctrl+Shift+N` (Windows)
3. Click **Export**
4. Save the HTML file

## 3. Run the Converter

### Easiest Way (Interactive):
```bash
python3 kindle_to_readwise.py
```
Then paste your file path when prompted.

### Quick Way (Command Line):
```bash
python3 kindle_to_readwise.py your_book.html
```

### Try the Example:
```bash
python3 kindle_to_readwise.py example.html
```

## 4. Import to Readwise

1. Go to [readwise.io/import](https://readwise.io/import)
2. Upload your `*_readwise.csv` file
3. Click **Confirm Import**
4. Done! 🎉

## Troubleshooting

**"Command not found: python3"**
- Try: `python kindle_to_readwise.py`
- Or install Python 3: [python.org](https://www.python.org/)

**"ModuleNotFoundError"**
- Run: `pip3 install -r requirements.txt`

**Need more help?**
- Read the full [Usage Guide](USAGE.md)
- Check [Troubleshooting section](README.md#troubleshooting)
- [Open an issue](https://github.com/sameerbajaj/kindle-to-readwise/issues)

---

That's it! For detailed documentation, see [README.md](README.md)
