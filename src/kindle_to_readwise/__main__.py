"""
Command-line interface for Kindle to Readwise converter.
"""

import sys
from .converter import process_kindle_export


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
