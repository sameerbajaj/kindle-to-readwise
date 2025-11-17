# Workflow

## Overview

This tool transforms Kindle HTML exports into beautifully formatted Readwise imports.

## The Process

```
┌─────────────────────────────────────────────────────────────────┐
│                        YOUR WORKFLOW                             │
└─────────────────────────────────────────────────────────────────┘

   📱 Kindle App                  🔧 This Tool              📚 Readwise
   ─────────────                  ──────────                ──────────
        │                              │                         │
        │  1. Export Notebook          │                         │
        │     (HTML file)              │                         │
        ├─────────────────────────────>│                         │
        │                              │                         │
        │                              │  2. Parse & Format      │
        │                              │     • Fix HTML          │
        │                              │     • Extract highlights│
        │                              │     • Add .h1 tags      │
        │                              │     • Add .favorite     │
        │                              │     • Attach notes      │
        │                              │     • Fill locations    │
        │                              │     • Fetch metadata    │
        │                              │                         │
        │                              │  3. Export CSV          │
        │                              ├────────────────────────>│
        │                              │                         │
        │                              │                         │  4. Import & Display
        │                              │                         │     • Bold headings
        │                              │                         │     • Starred favorites
        │                              │                         │     • Organized notes
        │                              │                         │
                                                                  📖 Beautiful Library!
```

## What Gets Transformed

### Input: Kindle HTML Export

```html
<div class="sectionHeading">Chapter 1: Introduction</div>
<div class="noteHeading">Highlight (yellow) - Page 15</div>
<div class="noteText">This is important.</div>
<div class="noteHeading">Note - Page 15</div>
<div class="noteText">My thoughts here.</div>

<div class="noteHeading">Highlight (pink) - Page 20</div>
<div class="noteText">Favorite quote!</div>
```

### ↓ Parsing & Transformation ↓

The tool:
1. **Fixes broken HTML** tags from Kindle
2. **Extracts** book title, author, chapters, highlights, notes
3. **Identifies** highlight types (yellow, pink, notes)
4. **Structures** data into sections and highlights
5. **Formats** for Readwise compatibility

### Output: Readwise CSV

```csv
Highlight,Title,Author,Note,Location,Date
"Chapter 1: Introduction","Book Title","Author",".h1",14,"2025-01-15 10:30:00"
"This is important.","Book Title","Author","My thoughts here.",15,"2025-01-15 10:30:00"
"Favorite quote!","Book Title","Author",".favorite",20,"2025-01-15 10:30:00"
```

### Result in Readwise

```
📕 Book Title by Author

    # Chapter 1: Introduction          ← Bold heading

    • This is important.               ← Regular highlight
      💭 My thoughts here.              ← Your note attached

    • Favorite quote!         ⭐       ← Starred favorite
```

## Feature Mapping

| Kindle Format | Tool Processing | Readwise Display |
|---------------|----------------|------------------|
| `<div class="sectionHeading">` | → `.h1` tag | **Bold Chapter Heading** |
| Yellow Highlight | → Standard entry | • Regular bullet |
| Pink Highlight | → `.favorite` tag | ⭐ Starred highlight |
| Note after Highlight | → Attached to previous | 💭 Indented note |
| Page numbers | → Fill missing gaps | Location preserved |
| Book metadata | → Google Books API | Clean title/author |

## Data Flow

```
Raw HTML
    ↓
fix_broken_html()
    ↓
BeautifulSoup parsing
    ↓
parse_highlights()
    ↓
Structured Dict
    ├─ title
    ├─ authors
    └─ sections[]
         ├─ sectionTitle
         └─ highlights[]
              ├─ highlight
              ├─ type
              └─ page
    ↓
convert_to_dataframe()
    ↓
Pandas DataFrame
    ├─ Add .h1 for sections
    ├─ Add .favorite for pink
    ├─ Attach notes
    └─ Fill locations
    ↓
get_book_metadata()
    ↓
Enhanced DataFrame
    ├─ Clean title
    └─ Proper author
    ↓
to_csv()
    ↓
Readwise CSV ✅
```

## Special Handling

### 1. Section Headings
```python
# Detected in HTML
<div class="sectionHeading">Chapter 1</div>

# Converted to
Highlight: "Chapter 1"
Note: ".h1"

# Displays in Readwise as
# Chapter 1  ← Bold heading
```

### 2. Pink Highlights (Favorites)
```python
# Detected in HTML
<div class="noteHeading">Highlight (pink) - Page 20</div>

# Converted to
Note: ".favorite"

# Displays in Readwise with
⭐ Star icon
```

### 3. Note Attachment
```python
# Sequential items in HTML
Highlight (yellow) - Page 15
"Important quote"
Note - Page 15
"My thoughts"

# Merged into
Highlight: "Important quote"
Note: "My thoughts"

# Displays as
• Important quote
  💭 My thoughts
```

### 4. Location Filling
```python
# Missing page numbers
Section heading     → Page ?
Highlight 1        → Page ?
Highlight 2        → Page 20
Highlight 3        → Page ?

# Backfilled to
Section heading    → Page 19
Highlight 1       → Page 19
Highlight 2       → Page 20
Highlight 3       → Page 19
```

## Why This Tool?

### Without This Tool
- ❌ Chapters are just regular highlights
- ❌ Pink highlights not marked as favorites
- ❌ Notes are separate entries
- ❌ Missing page numbers
- ❌ Messy metadata

### With This Tool
- ✅ Chapters are bold headings (`.h1`)
- ✅ Pink highlights starred (`.favorite`)
- ✅ Notes attached to highlights
- ✅ All locations filled
- ✅ Clean metadata from Google Books

## Integration Points

### Google Books API
```
Purpose: Fetch clean book metadata
Endpoint: https://www.googleapis.com/books/v1/volumes
Query: intitle:"book" inauthor:"author"
Returns: Proper title, author list, ISBN, cover
```

### Readwise CSV Format
```
Required Columns: Highlight, Title, Author
Optional Columns: Note, Location, Date, URL, Tags
Special Tags: .h1 (heading), .favorite (starred)
```

## Error Handling

The tool handles:
- ✅ Broken HTML from Kindle exports
- ✅ Missing page numbers
- ✅ Notes without highlights
- ✅ Empty sections
- ✅ Network failures (metadata)
- ✅ Invalid file formats
- ✅ Encoding issues

## Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Parse HTML | <1s | Even for 500+ highlights |
| Convert to DataFrame | <1s | Vectorized operations |
| Fetch metadata | 1-2s | Network dependent |
| Export CSV | <1s | Standard pandas export |
| **Total** | **2-4s** | Per book |

## Next Steps

After running the tool:

1. **Verify CSV**
   - Open in Excel/Numbers
   - Check for `.h1` tags
   - Verify `.favorite` tags
   - Confirm notes attached

2. **Upload to Readwise**
   - Go to readwise.io/import
   - Upload CSV
   - Preview import
   - Confirm

3. **Review in Readwise**
   - Check heading formatting
   - Verify starred highlights
   - Ensure notes attached
   - Set up daily review

---

For implementation details, see the [source code](kindle_to_readwise.py).
