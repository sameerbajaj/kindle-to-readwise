# Kindle to Readwise Converter 📚

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Convert your Kindle highlight exports to beautifully formatted Readwise imports with proper headings, notes, and structure.

**📖 [Quick Start](QUICKSTART.md) | 📚 [Usage Guide](USAGE.md) | 🔄 [Workflow](WORKFLOW.md) | 🤝 [Contributing](CONTRIBUTING.md)**

## Why This Tool?

While Readwise supports Kindle imports, this tool gives you:
- ✅ **Proper chapter headings** formatted as `.h1` tags in Readwise
- ✅ **Preserved highlight types** (including pink highlights as `.favorite`)
- ✅ **Attached notes** to their corresponding highlights
- ✅ **Clean metadata** fetched from Google Books API
- ✅ **Page/location numbers** properly filled and formatted
- ✅ **Easy-to-use** command-line tool or Python script

## Quick Start

### Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/sameerbajaj/kindle-to-readwise.git
   cd kindle-to-readwise
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Option 1: Interactive Mode (Easiest)

Simply run the script and follow the prompts:

```bash
python kindle_to_readwise.py
```

You'll be asked to:
1. Provide the path to your Kindle HTML export file
2. Choose whether to fetch metadata from Google Books

#### Option 2: Command Line

```bash
python kindle_to_readwise.py path/to/your/kindle_export.html
```

#### Option 3: Use as a Python Module

```python
from kindle_to_readwise import process_kindle_export

# Basic usage
csv_file = process_kindle_export('my_book.html')

# Advanced usage
csv_file = process_kindle_export(
    html_file_path='my_book.html',
    output_csv_path='custom_output.csv',
    fetch_metadata=True  # Get clean title/author from Google Books
)
```

## How to Export from Kindle

### On Kindle App (Mac/PC)
1. Open your Kindle app
2. Open the book you want to export
3. Go to **Notebook** (or press `Cmd/Ctrl + Shift + N`)
4. Click **Export** button
5. Save the HTML file

### On Kindle Device
1. Connect your Kindle to your computer via USB
2. Navigate to `Documents/My Clippings.txt`
3. Use Amazon's official export tool or convert manually

## What Gets Converted

The script converts your Kindle highlights into a CSV format that Readwise understands:

| Kindle Export | Readwise Format |
|---------------|-----------------|
| Chapter headings | `.h1` formatted headings |
| Yellow highlights | Regular highlights |
| Pink highlights | `.favorite` tagged highlights |
| Notes | Attached to their highlights |
| Page numbers | Preserved and filled for all entries |

## Output Format

The generated CSV includes these columns:
- **Highlight**: The highlighted text or chapter heading
- **Title**: Book title (cleaned via Google Books API)
- **Author**: Author name(s)
- **Note**: Tags (`.h1`, `.favorite`) or your notes
- **Location**: Page number or location
- **Date**: Export timestamp

## Example

**Before (Kindle HTML):**
```html
<div class="sectionHeading">Chapter 1: Introduction</div>
<div class="noteHeading">Highlight (yellow) - Page 15</div>
<div class="noteText">This is an important quote.</div>
<div class="noteHeading">Note - Page 15</div>
<div class="noteText">My thoughts on this quote.</div>
```

**After (Readwise CSV):**
```csv
Highlight,Title,Author,Note,Location,Date
"Chapter 1: Introduction","Book Title","Author Name",".h1",14,"2025-01-15 10:30:00"
"This is an important quote.","Book Title","Author Name","My thoughts on this quote.",15,"2025-01-15 10:30:00"
```

## Features in Detail

### 🎯 Smart Chapter Detection
Automatically identifies chapter headings and formats them as `.h1` tags, which Readwise renders as bold section headers.

### 📝 Note Attachment
Notes are automatically attached to their corresponding highlights instead of being separate entries.

### 💖 Highlight Type Preservation
Pink highlights from Kindle are tagged as `.favorite` in Readwise, making them stand out.

### 📍 Location Filling
Missing page numbers are intelligently filled based on surrounding highlights.

### 🌐 Metadata Enhancement
Fetches clean book metadata from Google Books API to ensure proper title and author formatting.

### 🧹 Text Cleanup
Removes formatting artifacts from Kindle exports (extra spaces, trailing characters, etc.)

## Troubleshooting

### "Invalid Kindle HTML format" error
- Make sure you're using an HTML export from Kindle's Notebook feature
- The file should contain elements with classes like `bodyContainer`, `bookTitle`, `noteHeading`

### "Could not fetch metadata from Google Books"
- This is not critical - the script will use the original title and author
- Check your internet connection
- Some books may not be in the Google Books database

### Missing highlights
- Verify your HTML export contains all expected highlights
- Check that highlights are properly formatted in the Kindle app before exporting

### CSV won't upload to Readwise
- Ensure the CSV has all required columns: Highlight, Title, Author
- Check that the file is not corrupted (open it in a text editor or Excel)
- Try re-exporting with `fetch_metadata=False` if metadata fetching causes issues

## Requirements

- Python 3.7 or higher
- pandas
- beautifulsoup4
- requests

See `requirements.txt` for specific versions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Some areas for improvement:

- [ ] Support for multiple HTML files at once (batch processing)
- [ ] GUI version for non-technical users
- [ ] Support for other e-reader formats (Kobo, Apple Books, etc.)
- [ ] Better error handling for malformed HTML
- [ ] Progress bar for large files
- [ ] Option to merge with existing Readwise libraries

## License

MIT License - feel free to use this for personal or commercial projects.

## Credits

Created by [Sameer Bajaj](https://github.com/sameerbajaj)

Inspired by the need for better-formatted Kindle imports in Readwise.

## Support

If you find this tool useful, please:
- ⭐ Star this repository
- 🐛 Report bugs via GitHub Issues
- 💡 Suggest features or improvements
- 📢 Share with other Readwise + Kindle users

## FAQ

**Q: Will this work with Kindle Unlimited books?**  
A: Yes, as long as you can export highlights from the Kindle app.

**Q: Can I use this for multiple books at once?**  
A: Currently, one book at a time. Batch processing is planned for a future update.

**Q: Does this work with Kindle cloud reader highlights?**  
A: Yes, export from the web reader's notebook and use that HTML file.

**Q: What about highlights from the Kindle e-reader device?**  
A: You'll need to export them as HTML first (use Amazon's export tool or convert `My Clippings.txt`).

**Q: Is my data sent anywhere?**  
A: Only to Google Books API (optional) for metadata. No highlights are sent anywhere.

**Q: Can I customize the output format?**  
A: Yes! Edit the `convert_to_dataframe()` function to adjust the formatting.

---

Made with ❤️ for book lovers and note-takers
