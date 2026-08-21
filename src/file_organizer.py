"""
Smart File Organizer

A command-line utility that automatically organizes files
into folders based on their file type.
"""

import argparse
import os
import shutil
from pathlib import Path

from src.config import FILE_CATEGORIES, DEFAULT_CATEGORY
from src.logger import setup_logger

def get_file_category(file_path):
    """
    Determine the category of a file based on its extension.

    Args:
        file_path (Path): Path to the file.

    Returns:
        str: Category name.
    """

    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return DEFAULT_CATEGORY


def create_category_folders(directory):
    """
    Create folders for all supported file categories.

    Args:
        directory (Path): Directory where folders should be created.

    Returns:
        dict: Category-to-folder mapping.
    """

    category_folders = {}

    categories = list(FILE_CATEGORIES.keys()) + [DEFAULT_CATEGORY]

    for category in categories:
        folder_path = directory / category

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        category_folders[category] = folder_path

    return category_folders


def get_unique_destination(destination):
    """
    Generate a unique destination path to prevent overwriting files.

    Example:
        report.pdf
        report_1.pdf
        report_2.pdf

    Args:
        destination (Path): Intended destination.

    Returns:
        Path: Safe destination path.
    """

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = f"{destination.stem}_{counter}{destination.suffix}"
        new_destination = destination.parent / new_name

        if not new_destination.exists():
            return new_destination

        counter += 1
def preview_files(directory):
    """
    Display the files that will be organized.

    Args:
        directory (Path): Directory to scan.

    Returns:
        list: Planned file movements.
    """

    planned_files = []

    for item in directory.iterdir():

        if not item.is_file():
            continue

        category = get_file_category(item)

        planned_files.append(
            {
                "file": item,
                "category": category,
            }
        )

    return planned_files
def confirm_operation(planned_files):
    """
    Display planned file movements and ask the user
    for confirmation.

    Args:
        planned_files (list): Planned file operations.

    Returns:
        bool: True if the user confirms, otherwise False.
    """

    if not planned_files:
        print("\nNo files found to organize.")
        return False

    print("\n" + "=" * 60)
    print("FILES TO BE ORGANIZED")
    print("=" * 60)

    for operation in planned_files:

        file_name = operation["file"].name
        category = operation["category"]

        print(
            f"{file_name:<35} -> {category}/"
        )

    print("=" * 60)

    response = input(
        "\nProceed with file organization? [y/N]: "
    ).strip().lower()

    return response in {"y", "yes"}


def organize_files(directory, dry_run=False, logger=None):
    """
    Organize files in a directory.

    Args:
        directory (Path): Target directory.
        dry_run (bool): Preview changes without moving files.
        logger (logging.Logger, optional): Application logger.

    Returns:
        dict: Detailed operation summary.
    """

    summary = {
        "scanned": 0,
        "organized": 0,
        "skipped": 0,
        "errors": 0,
        "categories": {},
    }

    # Only create folders when required.
    category_folders = {}

    for item in directory.iterdir():

        # Ignore directories.
        if not item.is_file():
            continue

        summary["scanned"] += 1

        category = get_file_category(item)

        # Track category statistics.
        summary["categories"][category] = (
            summary["categories"].get(category, 0) + 1
        )

        # Create the destination folder only when needed.
        if category not in category_folders:

            destination_folder = directory / category

            if not dry_run:
                try:
                    os.makedirs(
                        destination_folder,
                        exist_ok=True
                    )
                except OSError as error:
                    summary["errors"] += 1

                    print(
                        f"[ERROR] Could not create "
                        f"{category}/: {error}"
                    )

                    if logger:
                        logger.error(
                            "Could not create category folder %s: %s",
                            category,
                            error
                        )

                    continue

            category_folders[category] = destination_folder

        destination_folder = category_folders[category]
        destination = destination_folder / item.name

        # Prevent overwriting existing files.
        if not dry_run:
            destination = get_unique_destination(destination)

        try:

            if dry_run:

                print(
                    f"[DRY RUN] "
                    f"{item.name} -> {category}/"
                )

                if logger:
                    logger.info(
                        "[DRY RUN] %s -> %s/",
                        item.name,
                        category
                    )

            else:

                shutil.move(
                    str(item),
                    str(destination)
                )

                print(
                    f"[MOVED] "
                    f"{item.name} -> {category}/"
                )

                if logger:
                    logger.info(
                        "Moved %s -> %s/",
                        item.name,
                        category
                    )

            summary["organized"] += 1

        except OSError as error:

            summary["errors"] += 1

            print(
                f"[ERROR] "
                f"Could not process {item.name}: {error}"
            )

            if logger:
                logger.error(
                    "Could not process %s: %s",
                    item.name,
                    error
                )

    return summary


def print_summary(summary, dry_run=False):
    """Display a detailed summary of the organization operation."""

    print("\n" + "=" * 60)

    if dry_run:
        print("SMART FILE ORGANIZER - DRY RUN")
    else:
        print("SMART FILE ORGANIZER - COMPLETE")

    print("=" * 60)

    print(f"Files scanned:    {summary['scanned']}")
    print(f"Files organized:  {summary['organized']}")
    print(f"Files skipped:    {summary['skipped']}")
    print(f"Errors:           {summary['errors']}")

    if summary["categories"]:

        print("\nFiles by category:")

        for category, count in sorted(
            summary["categories"].items()
        ):
            print(
                f"  {category:<16} {count}"
            )

    if dry_run:
        print("\nNo files were moved.")

    print("=" * 60)


def parse_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Smart File Organizer - automatically organize files by type."
    )

    parser.add_argument(
        "--directory",
        "-d",
        required=True,
        help="Directory containing the files to organize."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview file movements without changing any files."
    )

    return parser.parse_args()

def main():
    """Application entry point."""

    logger = setup_logger()

    args = parse_arguments()

    directory = Path(
        args.directory
    ).expanduser().resolve()

    if not directory.exists():

        print(
            "ERROR: Directory does not exist."
        )

        return

    if not directory.is_dir():

        print(
            "ERROR: The specified path "
            "is not a directory."
        )

        return

    planned_files = preview_files(
        directory
    )

    if args.dry_run:

        summary = organize_files(
            directory=directory,
            dry_run=True,
            logger=logger
        )

        print_summary(
            summary=summary,
            dry_run=True
        )

        return

    if not confirm_operation(
        planned_files
    ):

        print(
            "\nOperation cancelled. "
            "No files were moved."
        )

        logger.info(
            "File organization cancelled by user."
        )

        return

    summary = organize_files(
        directory=directory,
        dry_run=False,
        logger=logger
    )

    print_summary(
        summary=summary,
        dry_run=False
    )


if __name__ == "__main__":
    main()