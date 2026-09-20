import argparse
import logging
import os
import shutil
from pathlib import Path

# Configure file extension mapping
EXTENSION_MAP = {
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx", ".csv", ".epub"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp", ".webp", ".ico"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar", ".iso"],
    "Executables": [".exe", ".msi", ".dmg", ".sh", ".deb", ".bat"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".c", ".java", ".json"]
}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def organize_directory(target_path: Path, dry_run: bool = False):
    """
    Scans the target directory and moves files into organized subdirectories.
    """
    if not target_path.exists():
        logging.error(f"Target directory does not exist: {target_path}")
        return

    if not target_path.is_dir():
        logging.error(f"Specified path is not a directory: {target_path}")
        return

    logging.info(f"Starting organization for directory: {target_path.resolve()}")
    moved_count = 0

    for item in target_path.iterdir():
        # Ignore subdirectories to prevent nested reorganization loops
        if item.is_dir():
            continue

        file_ext = item.suffix.lower()
        destination_category = "Others"

        # Determine target folder based on extension mapping
        for category, extensions in EXTENSION_MAP.items():
            if file_ext in extensions:
                destination_category = category
                break

        dest_folder = target_path / destination_category
        target_file_path = dest_folder / item.name

        if dry_run:
            logging.info(f"[DRY-RUN] Would move: '{item.name}' -> '{destination_category}/'")
        else:
            dest_folder.mkdir(exist_ok=True)
            # Prevent overwriting if a file with the same name exists
            if target_file_path.exists():
                stem = item.stem
                suffix = item.suffix
                target_file_path = dest_folder / f"{stem}_copy{suffix}"

            shutil.move(str(item), str(target_file_path))
            logging.info(f"Moved: '{item.name}' -> '{destination_category}/'")
            moved_count += 1

    if not dry_run:
        logging.info(f"Organization completed. Total files moved: {moved_count}")

def main():
    parser = argparse.ArgumentParser(
        description="Smart File Organizer CLI Tool - Automatically organizes files into structured directories."
    )
    parser.add_argument(
        "-p", "--path",
        type=str,
        default=".",
        help="Path to the directory to organize (default: current directory)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the organization process without moving any files"
    )

    args = parser.parse_args()
    target = Path(args.path)
    organize_directory(target, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
