"""
Helper utility functions for the project.

General-purpose utility functions used across multiple modules.
"""

import os
import psutil
from pathlib import Path
from typing import Union


def ensure_directory_exists(directory: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Path to the directory
    
    Returns:
        Path object of the directory
    
    Example:
        >>> path = ensure_directory_exists('data/processed/results')
        >>> print(path)
        data/processed/results
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def get_memory_usage() -> dict[str, float]:
    """
    Get current memory usage statistics.
    
    Returns:
        Dictionary with memory usage in GB and percentage
    
    Example:
        >>> mem = get_memory_usage()
        >>> print(f"Using {mem['used_gb']:.2f} GB ({mem['percent']:.1f}%)")
    """
    mem = psutil.virtual_memory()
    return {
        'total_gb': mem.total / (1024 ** 3),
        'available_gb': mem.available / (1024 ** 3),
        'used_gb': mem.used / (1024 ** 3),
        'percent': mem.percent
    }


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes into human-readable string.
    
    Args:
        bytes_value: Number of bytes
    
    Returns:
        Formatted string (e.g., "1.5 GB", "200 MB")
    
    Example:
        >>> print(format_bytes(1073741824))
        1.00 GB
        >>> print(format_bytes(1048576))
        1.00 MB
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def get_file_size(filepath: Union[str, Path]) -> str:
    """
    Get formatted file size.
    
    Args:
        filepath: Path to the file
    
    Returns:
        Formatted file size string
    
    Example:
        >>> size = get_file_size('data/raw/accidents.csv')
        >>> print(size)
        2.5 GB
    """
    filepath = Path(filepath)
    if not filepath.exists():
        return "File not found"
    
    size_bytes = filepath.stat().st_size
    return format_bytes(size_bytes)


def split_list_into_chunks(lst: list, chunk_size: int) -> list[list]:
    """
    Split a list into chunks of specified size.
    
    Args:
        lst: List to split
        chunk_size: Size of each chunk
    
    Returns:
        List of chunked lists
    
    Example:
        >>> data = list(range(10))
        >>> chunks = split_list_into_chunks(data, 3)
        >>> print(chunks)
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def count_lines_in_file(filepath: Union[str, Path]) -> int:
    """
    Count the number of lines in a file.
    
    Args:
        filepath: Path to the file
    
    Returns:
        Number of lines
    
    Example:
        >>> n_lines = count_lines_in_file('data/raw/accidents.csv')
        >>> print(f"File has {n_lines:,} lines")
    """
    filepath = Path(filepath)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return sum(1 for _ in f)


def print_section_header(text: str, width: int = 80, char: str = '=') -> None:
    """
    Print a formatted section header.
    
    Args:
        text: Header text
        width: Total width of the header
        char: Character to use for the border
    
    Example:
        >>> print_section_header("Data Loading")
        ================================ Data Loading ================================
    """
    text = f" {text} "
    padding = (width - len(text)) // 2
    header = char * padding + text + char * padding
    if len(header) < width:
        header += char * (width - len(header))
    print(f"\n{header}\n")


if __name__ == "__main__":
    # Test utility functions
    print_section_header("Testing Utility Functions")
    
    # Test directory creation
    test_dir = ensure_directory_exists('test_output/tmp')
    print(f"Created directory: {test_dir}")
    
    # Test memory usage
    mem = get_memory_usage()
    print(f"\nMemory usage: {mem['used_gb']:.2f} GB / {mem['total_gb']:.2f} GB ({mem['percent']:.1f}%)")
    
    # Test format bytes
    print("\nFormatting bytes:")
    print(f"  1 KB: {format_bytes(1024)}")
    print(f"  1 MB: {format_bytes(1024**2)}")
    print(f"  1 GB: {format_bytes(1024**3)}")
    
    # Test list chunking
    data = list(range(10))
    chunks = split_list_into_chunks(data, 3)
    print(f"\nChunked {data} into: {chunks}")
    
    # Cleanup
    test_dir.rmdir()
