# utils.py

def clean_text(text):
    """
    Cleans text by removing non-UTF-8 characters and normalizing spaces.
    
    Args:
        text: The text string to clean.
        
    Returns:
        Cleaned text as a UTF-8 compatible string.
    """
    # Normalize spaces and remove non-UTF-8 characters
    clean_text = text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
    
    # Replace any problematic characters, e.g., Windows-specific quotes, dashes, etc.
    replacements = {
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        '\u201c': '"',  # Left double quotation mark
        '\u201d': '"',  # Right double quotation mark
        '\u2013': '-',  # En dash
        '\u2014': '-',  # Em dash
        # Add more replacements as needed
    }
    for char, replacement in replacements.items():
        clean_text = clean_text.replace(char, replacement)
    
    # Remove non-printable or control characters
    clean_text = ''.join(c for c in clean_text if c.isprintable())

    return clean_text
