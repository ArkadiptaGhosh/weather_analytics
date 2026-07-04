import json
from pathlib import Path


class FileManager:
    """Handles file read and write operations."""

    def __init__(self):
        """Initialize the File Manager."""

    def save_json(self, data, file_path):
        """Save JSON data to a file."""

        path = Path(file_path)

        # Create the parent directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w") as file:
            json.dump(data, file, indent=4)