"""
Color utility for terminal output formatting
Makes console output more readable with colored headers
"""

def header(text, color="yellow"):
    """
    Print a colored header with separator lines
    
    Args:
        text: The header text to display
        color: Color name (yellow, cyan, green, red, blue)
    """
    colors = {
        "yellow": "\033[1;33m",
        "cyan": "\033[1;36m",
        "green": "\033[1;32m",
        "red": "\033[1;31m",
        "blue": "\033[1;34m",
        "reset": "\033[0m"
    }
    
    color_code = colors.get(color.lower(), colors["yellow"])
    reset = colors["reset"]
    separator = "=" * (len(text) + 4)
    
    print(f"\n{color_code}{separator}")
    print(f"  {text}  ")
    print(f"{separator}{reset}\n")
