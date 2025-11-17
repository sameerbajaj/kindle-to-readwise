"""
Kindle to Readwise Converter
Convert Kindle HTML highlight exports to Readwise-compatible CSV format.
"""

__version__ = "1.0.0"
__author__ = "Sameer Bajaj"

from .converter import (
    process_kindle_export,
    parse_highlights,
    convert_to_dataframe,
    get_book_metadata,
)

__all__ = [
    "process_kindle_export",
    "parse_highlights",
    "convert_to_dataframe",
    "get_book_metadata",
]
