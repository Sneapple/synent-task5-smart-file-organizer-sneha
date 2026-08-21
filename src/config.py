"""
Configuration for the Smart File Organizer.

This module contains the file-extension mappings used to determine
which category a file belongs to.
"""

FILE_CATEGORIES = {
    "Images": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico", ".tiff"
    },

    "Documents": {
        ".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".tex"
    },

    "Videos": {
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v"
    },

    "Audio": {
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"
    },

    "Spreadsheets": {
        ".xls", ".xlsx", ".csv", ".ods", ".tsv"
    },

    "Presentations": {
        ".ppt", ".pptx", ".odp", ".key"
    },

    "Archives": {
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"
    },

    "Code": {
        ".py", ".js", ".jsx", ".ts", ".tsx", ".java",
        ".c", ".cpp", ".h", ".hpp", ".cs",
        ".html", ".css", ".scss", ".sql",
        ".php", ".go", ".rs", ".rb", ".sh", ".bat"
    },
}


DEFAULT_CATEGORY = "Others"