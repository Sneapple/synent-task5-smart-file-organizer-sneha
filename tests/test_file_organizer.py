"""
Automated tests for the Smart File Organizer.
"""

import tempfile
import unittest

from pathlib import Path

from src.file_organizer import (
    get_file_category,
    get_unique_destination,
    create_category_folders,
    organize_files,
)


class TestFileCategory(unittest.TestCase):
    """Tests for file category detection."""

    def test_image_file(self):
        file_path = Path("photo.jpg")

        self.assertEqual(
            get_file_category(file_path),
            "Images"
        )

    def test_document_file(self):
        file_path = Path("report.pdf")

        self.assertEqual(
            get_file_category(file_path),
            "Documents"
        )

    def test_video_file(self):
        file_path = Path("movie.mp4")

        self.assertEqual(
            get_file_category(file_path),
            "Videos"
        )

    def test_unknown_file(self):
        file_path = Path("unknown.xyz")

        self.assertEqual(
            get_file_category(file_path),
            "Others"
        )

    def test_uppercase_extension(self):
        file_path = Path("PHOTO.JPG")

        self.assertEqual(
            get_file_category(file_path),
            "Images"
        )


class TestDuplicateHandling(unittest.TestCase):
    """Tests for duplicate filename protection."""

    def test_unique_destination_when_file_does_not_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:

            destination = (
                Path(temp_dir) / "report.pdf"
            )

            result = get_unique_destination(destination)

            self.assertEqual(
                result,
                destination
            )

    def test_duplicate_destination(self):
        with tempfile.TemporaryDirectory() as temp_dir:

            temp_path = Path(temp_dir)

            original = temp_path / "report.pdf"
            original.touch()

            result = get_unique_destination(original)

            self.assertEqual(
                result.name,
                "report_1.pdf"
            )

    def test_multiple_duplicates(self):
        with tempfile.TemporaryDirectory() as temp_dir:

            temp_path = Path(temp_dir)

            (temp_path / "report.pdf").touch()
            (temp_path / "report_1.pdf").touch()

            result = get_unique_destination(
                temp_path / "report.pdf"
            )

            self.assertEqual(
                result.name,
                "report_2.pdf"
            )


class TestFolderCreation(unittest.TestCase):
    """Tests for category folder creation."""

    def test_category_folders_are_created(self):

        with tempfile.TemporaryDirectory() as temp_dir:

            directory = Path(temp_dir)

            folders = create_category_folders(
                directory
            )

            self.assertIn(
                "Images",
                folders
            )

            self.assertTrue(
                (directory / "Images").exists()
            )

            self.assertTrue(
                (directory / "Documents").exists()
            )

            self.assertTrue(
                (directory / "Videos").exists()
            )


class TestFileOrganization(unittest.TestCase):
    """Tests for actual file organization."""

    def test_files_are_moved_to_correct_categories(self):

        with tempfile.TemporaryDirectory() as temp_dir:

            directory = Path(temp_dir)

            image = directory / "photo.jpg"
            document = directory / "resume.pdf"
            video = directory / "movie.mp4"

            image.touch()
            document.touch()
            video.touch()

            summary = organize_files(
                directory
            )

            self.assertEqual(
                summary["scanned"],
                3
            )

            self.assertEqual(
                summary["organized"],
                3
            )

            self.assertTrue(
                (directory / "Images" / "photo.jpg").exists()
            )

            self.assertTrue(
                (
                    directory
                    / "Documents"
                    / "resume.pdf"
                ).exists()
            )

            self.assertTrue(
                (
                    directory
                    / "Videos"
                    / "movie.mp4"
                ).exists()
            )

    def test_unknown_file_goes_to_others(self):

        with tempfile.TemporaryDirectory() as temp_dir:

            directory = Path(temp_dir)

            unknown_file = (
                directory / "mystery.xyz"
            )

            unknown_file.touch()

            organize_files(directory)

            self.assertTrue(
                (
                    directory
                    / "Others"
                    / "mystery.xyz"
                ).exists()
            )

    def test_dry_run_does_not_move_files(self):

        with tempfile.TemporaryDirectory() as temp_dir:

            directory = Path(temp_dir)

            image = directory / "photo.jpg"
            image.touch()

            summary = organize_files(
                directory,
                dry_run=True
            )

            self.assertEqual(
                summary["scanned"],
                1
            )

            self.assertEqual(
                summary["organized"],
                1
            )

            # Original file must still exist.
            self.assertTrue(
                image.exists()
            )

            # Destination must NOT exist.
            self.assertFalse(
                (
                    directory
                    / "Images"
                    / "photo.jpg"
                ).exists()
            )


if __name__ == "__main__":
    unittest.main()