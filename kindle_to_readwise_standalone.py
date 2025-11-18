#!/usr/bin/env python3
"""
Kindle to Readwise Converter - Backward Compatibility Wrapper

This script is maintained for backward compatibility.
For new installations, please use the package: pip install git+https://github.com/sameerbajaj/kindle-to-readwise

Author: Sameer Bajaj
Repository: https://github.com/sameerbajaj/kindle-to-readwise
License: MIT
Version: 1.0.0
"""

import sys

# Try to use the installed package, fall back to bundled version
try:
    from kindle_to_readwise.__main__ import main
    if __name__ == "__main__":
        main()
except ImportError:
    # Package not installed, use the bundled code
    import re
    import os
    import pandas as pd
    import requests
    from datetime import datetime
    from bs4 import BeautifulSoup, NavigableString


def fix_broken_html(source_html):
    """
    Fix broken HTML tags from Kindle export.
    Kindle exports often have mismatched closing tags that need correction.
    """
    fixed_html = re.sub(r'(\r\n|\n|\r)', '', source_html)
    fixed_html = fixed_html.replace("</div></div></h1><hr/>", "</div></h1><hr/>")

    if "</h3>" not in fixed_html:
        return fixed_html

    fixed_html = fixed_html.replace("</h3>", "</div>").replace(
        "</div><div class='noteText'>", "</h3><div class='noteText'>"
    )
    return fixed_html


def highlight_type(text):
    """Extract the type of highlight from heading text."""
    match = re.match(r'^(.*)\s-\s', text)
    if match:
        return match.group(1)
    return None


def extract_page_number(text):
    """Extract page number from heading text."""
    match = re.search(r'Page\s+(\d+)', text)
    if match:
        return match.group(1)
    return None


def clean_up_text(text):
    """
    Remove extra spaces before punctuation.
    Kindle exports sometimes add spaces before punctuation marks.
    """
    new_text = text
    marks = [",", ".", ";", "(", ")", '"']
    for mark in marks:
        new_text = new_text.replace(f' {mark}', mark)
    return new_text


def parse_highlights(raw_html):
    """
    Parse Kindle HTML export into structured data.
    
    Returns:
        dict: Contains book title, authors, and sections with highlights
    """
    fixed_html = fix_broken_html(raw_html)
    soup = BeautifulSoup(fixed_html, 'html.parser')

    container = soup.find(class_='bodyContainer')
    if not container:
        raise ValueError("Invalid Kindle HTML format. Could not find bodyContainer.")
    
    book_title = soup.find(class_='bookTitle')
    book_title = book_title.text.strip() if book_title else 'Unknown Title'
    
    book_authors = soup.find(class_='authors')
    book_authors = book_authors.text.strip() if book_authors else 'Unknown Author'

    sections = []
    current_section = None
    current_highlight = None

    for node in container.children:
        if isinstance(node, NavigableString):
            continue

        class_list = node.get('class', [])
        
        if 'sectionHeading' in class_list:
            if current_section is not None:
                sections.append(dict(current_section))
            
            current_section = {
                'sectionTitle': node.text.strip(),
                'highlights': []
            }

        if 'noteHeading' in class_list:
            heading = node.text.strip()
            current_highlight = {
                'type': highlight_type(heading),
                'page': extract_page_number(heading),
                'highlight': ''
            }

        if 'noteText' in class_list:
            if current_highlight is None:
                continue

            # Clean the highlight text
            highlight_text = node.text.strip()
            if highlight_text.endswith('['):
                highlight_text = highlight_text[:-1].strip()

            current_highlight['highlight'] = clean_up_text(highlight_text)
            current_section['highlights'].append(dict(current_highlight))

    if current_section is not None:
        sections.append(dict(current_section))

    return {
        'title': book_title,
        'authors': book_authors,
        'sections': sections
    }


def convert_to_dataframe(parsed_highlights):
    """
    Convert parsed highlights to DataFrame formatted for Readwise import.
    
    The DataFrame follows Readwise CSV format:
    - Highlight: The text of the highlight or section heading
    - Title: Book title
    - Author: Book author(s)
    - Note: Special tags (.h1 for headings, .favorite for pink highlights) or user notes
    - Location: Page number or location in the book
    - Date: Timestamp of export
    """
    data = []
    
    title = parsed_highlights['title']
    authors = parsed_highlights['authors']
    
    for section in parsed_highlights['sections']:
        section_title = section['sectionTitle']
        
        # Add section title as a .h1 note (Readwise heading format)
        data.append({
            'Highlight': section_title,
            'Title': title,
            'Author': authors,
            'Note': '.h1',
            'Location': pd.NA
        })
        
        for highlight in section['highlights']:
            highlight_text = highlight['highlight']
            highlight_page = highlight.get('page', pd.NA)
            highlight_type_val = highlight['type']
            
            # Handle Note types - attach them to the previous highlight
            if highlight_type_val == 'Note':
                if data:
                    if data[-1]['Note'] == '.favorite':
                        data[-1]['Note'] += f' {highlight_text}'
                    else:
                        data[-1]['Note'] = highlight_text
            else:
                # Add new highlight entry
                data.append({
                    'Highlight': highlight_text,
                    'Location': highlight_page,
                    'Title': title,
                    'Author': authors,
                    'Note': '.favorite' if highlight_type_val == 'Highlight (pink)' else ''
                })
    
    # Create DataFrame
    df = pd.DataFrame(data)

    # Fill missing Location values using backfill strategy
    df['Location'] = pd.to_numeric(df['Location'], errors='coerce')
    filled_locations = df['Location'].bfill()
    is_na = df['Location'].isna()
    df.loc[is_na, 'Location'] = filled_locations[is_na] - 1
    df['Location'] = df['Location'].clip(lower=1)
    df['Location'] = df['Location'].astype(pd.Int64Dtype())
    
    # Add current date
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df['Date'] = current_date
    
    return df


def get_book_metadata(title_query, authors_query):
    """
    Fetch book metadata from Google Books API.
    
    Returns:
        tuple: (title, author) with proper formatting
    """
    search_query = f'intitle:"{title_query}" inauthor:"{authors_query}"'
    params = {'q': search_query}
    
    try:
        response = requests.get('https://www.googleapis.com/books/v1/volumes', params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if 'items' in data and data['items']:
            for item in data['items']:
                volume_info = item.get('volumeInfo', {})
                api_title = volume_info.get('title', 'Unknown Title')
                api_authors_list = volume_info.get('authors', ['Unknown Author'])
                api_authors_str = ', '.join(api_authors_list)

                title_match = title_query.lower() in api_title.lower()
                author_match = any(authors_query.lower() in author.lower() for author in api_authors_list)

                if title_match and author_match:
                    return api_title, api_authors_str
            
            # If no exact match, return first result
            first_item = data['items'][0]['volumeInfo']
            return (
                first_item.get('title', title_query),
                ', '.join(first_item.get('authors', [authors_query]))
            )
        
        return title_query, authors_query

    except Exception as e:
        print(f"⚠️  Could not fetch metadata from Google Books: {e}")
        print(f"   Using original title and author from Kindle export.")
        return title_query, authors_query


def process_kindle_export(html_file_path, output_csv_path=None, fetch_metadata=True):
    """
    Main function to process Kindle HTML export and create Readwise CSV.
    
    Args:
        html_file_path: Path to the Kindle HTML export file
        output_csv_path: Optional path for output CSV (auto-generated if not provided)
        fetch_metadata: Whether to fetch metadata from Google Books API
    
    Returns:
        str: Path to the generated CSV file
    """
    # Validate input file
    if not os.path.exists(html_file_path):
        raise FileNotFoundError(f"HTML file not found: {html_file_path}")
    
    # Auto-generate output filename if not provided
    if output_csv_path is None:
        base_name = os.path.splitext(html_file_path)[0]
        output_csv_path = f"{base_name}_readwise.csv"
    
    print(f"📚 Reading Kindle export: {html_file_path}")
    
    # Read and parse HTML
    with open(html_file_path, 'r', encoding='utf-8') as file:
        raw_html = file.read()
    
    print("🔍 Parsing highlights...")
    parsed_highlights = parse_highlights(raw_html)
    
    print(f"   Found: {parsed_highlights['title']}")
    print(f"   Author: {parsed_highlights['authors']}")
    print(f"   Sections: {len(parsed_highlights['sections'])}")
    total_highlights = sum(len(s['highlights']) for s in parsed_highlights['sections'])
    print(f"   Total highlights: {total_highlights}")
    
    # Convert to DataFrame
    print("\n📊 Converting to Readwise format...")
    df_highlights = convert_to_dataframe(parsed_highlights)
    
    # Optionally fetch metadata from Google Books
    if fetch_metadata:
        print("🌐 Fetching book metadata from Google Books...")
        clean_title, clean_author = get_book_metadata(
            parsed_highlights['title'],
            parsed_highlights['authors']
        )
        df_highlights['Title'] = clean_title
        df_highlights['Author'] = clean_author
        print(f"   Updated title: {clean_title}")
        print(f"   Updated author: {clean_author}")
    
    # Export to CSV
    df_highlights.to_csv(output_csv_path, index=False)
    print(f"\n✅ CSV exported successfully: {output_csv_path}")
    print(f"   Total rows: {len(df_highlights)}")
    print(f"\n🎉 Ready to upload to Readwise!")
    print(f"   Visit: https://readwise.io/import")
    
    return output_csv_path


def main():
    """Command-line interface for the converter."""
    print("=" * 60)
    print("Kindle to Readwise Converter")
    print("=" * 60)
    print()
    
    # Check if file path was provided as argument
    if len(sys.argv) > 1:
        html_file = sys.argv[1]
    else:
        # Interactive mode
        print("Please provide the path to your Kindle HTML export file.")
        print("(Drag and drop the file here, or type the path)")
        print()
        html_file = input("HTML file path: ").strip()
        
        # Remove quotes if user dragged and dropped
        html_file = html_file.strip('"').strip("'")
    
    if not html_file:
        print("❌ Error: No file path provided.")
        sys.exit(1)
    
    # Ask about metadata fetching
    if len(sys.argv) <= 2:
        print("\nFetch book metadata from Google Books? (recommended)")
        print("This will clean up the book title and author name.")
        fetch_meta = input("Fetch metadata? (y/n) [y]: ").strip().lower()
        fetch_metadata = fetch_meta != 'n'
    else:
        fetch_metadata = True
    
    try:
        output_file = process_kindle_export(html_file, fetch_metadata=fetch_metadata)
        print(f"\n📁 Output file: {output_file}")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure this is a valid Kindle HTML export file.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("   Please report this issue on GitHub with your error message.")
        sys.exit(1)


if __name__ == "__main__":
    main()
