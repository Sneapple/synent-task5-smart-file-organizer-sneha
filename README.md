# Smart File Organizer

A Python-based command-line automation tool that automatically organizes files into categorized folders based on their file extensions.

This project was developed as part of the **Synent Technologies Python Development Internship Program – Task 5**.

---

## Overview

The Smart File Organizer helps users clean up cluttered directories such as Downloads by automatically sorting files into meaningful categories.

Instead of manually moving files one by one, the application scans a directory, identifies each file type, creates the required folders, and safely moves the files.

The application also includes:

- Dry-run preview mode
- User confirmation before file movement
- Duplicate filename protection
- Operation logging
- Input validation
- Error handling
- Category statistics
- Automated unit tests
- Command-line interface

---

## Features

### File Categorization

The application supports multiple file categories:

| Category | Examples |
|---|---|
| Images | JPG, PNG, GIF, SVG, WEBP |
| Documents | PDF, DOC, DOCX, TXT, RTF |
| Videos | MP4, MKV, AVI, MOV, WMV |
| Audio | MP3, WAV, AAC, FLAC, OGG |
| Spreadsheets | XLS, XLSX, CSV, ODS |
| Presentations | PPT, PPTX, ODP |
| Archives | ZIP, RAR, 7Z, TAR, GZ |
| Code | PY, JS, JAVA, HTML, CSS, SQL |
| Others | Unknown or unsupported file types |

---

## Synent Task 5 Requirements

The project satisfies all required internship features:

- [x] Automatically organize files
- [x] Uses Python `os` module
- [x] Uses Python `shutil` module
- [x] Sort files by type
- [x] Images category
- [x] Documents category
- [x] Videos category
- [x] Automatically create folders
- [x] Produce a clean directory structure
- [x] Fully functional application

---

## Additional Features

The basic internship requirements were extended with several real-world features.

### Dry Run

Users can preview file movements without changing anything.

```bash
python -m src.file_organizer --directory sample_data --dry-run

Example:

[DRY RUN] photo.jpg -> Images/
[DRY RUN] resume.pdf -> Documents/
[DRY RUN] movie.mp4 -> Videos/


No files were moved.
User Confirmation

Normal execution displays the files that will be organized and asks for confirmation before moving them.

FILES TO BE ORGANIZED
============================================================


photo.jpg                         -> Images/
resume.pdf                        -> Documents/
movie.mp4                         -> Videos/


============================================================


Proceed with file organization? [y/N]:

The operation is cancelled safely if the user does not confirm.

Duplicate File Protection

The application prevents accidental overwriting of existing files.

For example:

report.pdf
report_1.pdf
report_2.pdf

If report.pdf already exists, a unique filename is automatically generated.

Logging

File operations are recorded in:

logs/organizer.log

Example:

2026-08-21 11:30:12 | INFO | Moved photo.jpg -> Images/
2026-08-21 11:30:12 | INFO | Moved resume.pdf -> Documents/

Logs are excluded from GitHub using .gitignore.

Input Validation

The application checks whether the supplied path:

Exists
Is a directory
Can be accessed

Invalid paths are handled without exposing unnecessary Python tracebacks to the user.

Statistics

After processing, the application displays a summary:

============================================================
SMART FILE ORGANIZER - COMPLETE
============================================================
Files scanned:    9
Files organized:  9
Files skipped:    0
Errors:           0


Files by category:
  Archives         1
  Audio            1
  Code             1
  Documents        1
  Images           1
  Others           1
  Presentations    1
  Spreadsheets     1
  Videos           1
============================================================
How It Works

The application follows this workflow:

User selects directory
        ↓
Validate directory
        ↓
Scan files
        ↓
Identify file extension
        ↓
Determine category
        ↓
Preview planned operations
        ↓
User confirmation
        ↓
Create required category folder
        ↓
Check for duplicate filename
        ↓
Move file using shutil
        ↓
Record operation in log
        ↓
Display summary
Project Structure
synent-task5-smart-file-organizer-sneha/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── file_organizer.py
│   └── logger.py
│
├── tests/
│   ├── __init__.py
│   └── test_file_organizer.py
│
├── sample_data/
│   └── .gitkeep
│
└── screenshots/
    └── .gitkeep
Technologies Used
Python 3
os
shutil
pathlib
argparse
logging
unittest

No third-party Python packages are required.

Installation
1. Clone the repository
git clone <YOUR-GITHUB-REPOSITORY-URL>
2. Navigate into the project
cd synent-task5-smart-file-organizer-sneha
3. Verify Python
python --version

Python 3.x is required.

Usage
Standard organization
python -m src.file_organizer --directory sample_data

The application displays the files it intends to move and asks for confirmation.

Enter:

y

to proceed.

Dry Run

To preview operations without moving files:

python -m src.file_organizer --directory sample_data --dry-run
Command Help
python -m src.file_organizer --help
Testing

The project includes automated unit tests covering:

File categorization
Uppercase extensions
Unknown file types
Duplicate filenames
Multiple duplicate filenames
Folder creation
File movement
Dry-run behavior

Run all tests with:

python -m unittest discover -s tests -v

Expected result:

Ran 12 tests


OK
Safety Considerations

The application was designed to reduce the risk of unintended file operations.

Safety mechanisms include:

Dry-run mode
Preview before execution
User confirmation
Duplicate filename protection
Directory validation
Error handling
Operation logging

The application should initially be tested on a dedicated test directory before being used on important personal files.

Future Improvements

Potential future versions could include:

GUI interface
Recursive directory organization
Configurable categories
Custom extension configuration
Scheduled automatic organization
File size and date-based rules
Undo functionality
Configuration file support
Cross-platform packaging
Windows executable distribution
Learning Outcomes

This project provided practical experience with:

Python programming
File-system automation
os and shutil
Object-oriented and modular programming concepts
Command-line interfaces
Exception handling
Logging
Input validation
Automated testing
Git and GitHub workflow
Defensive programming
Internship

Synent Technologies – Python Development Internship Program

Task: Task 5 – File Organizer

The project was developed as an extension of the internship requirements with additional real-world functionality and testing.

Author

Sneha Munigala




