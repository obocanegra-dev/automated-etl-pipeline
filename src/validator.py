import re
import os
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class FileValidator:
    def __init__(self):
        # Target format: ID_TYPE_DATE.ext
        # Example: 1001_LAB_20231025.pdf
        self.name_pattern = re.compile(r"^(\d+)_([A-Z]+)_(\d{8})\.(.+)$")
        
        # Whitelisted extensions
        self.allowed_extensions = {'.pdf', '.jpg', '.png', '.docx', '.txt'}

    def validate_name(self, filename: str) -> bool:
        """
        Checks if the filename matches the global standard pattern.
        """
        return bool(self.name_pattern.match(filename))

    def normalize(self, filename: str) -> Tuple[bool, str, Optional[str]]:
        """
        Attempts to normalize the filename.
        Returns (is_valid, new_filename_or_original, error_reason)
        """
        if self.validate_name(filename):
            # Check extension
            _, ext = os.path.splitext(filename)
            if ext.lower() not in self.allowed_extensions:
                return False, filename, f"Extension {ext} not allowed"
            return True, filename, None
        
        # In a real scenario, we might have logic here to fix common bad patterns.
        # For now, if it doesn't match strict regex, we reject it.
        return False, filename, "Does not match ID_TYPE_DATE format"

    def get_metadata(self, filename: str) -> dict:
        """
        Extracts metadata from a valid filename.
        """
        match = self.name_pattern.match(filename)
        if match:
            return {
                "id": match.group(1),
                "type": match.group(2),
                "date": match.group(3),
                "ext": match.group(4)
            }
        return {}
