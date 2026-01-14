import os
import shutil
import logging
from typing import List

logger = logging.getLogger(__name__)

class FileExtractor:
    def __init__(self, source_dir: str):
        self.source_dir = source_dir
        if not os.path.exists(self.source_dir):
            os.makedirs(self.source_dir)

    def scan_for_files(self) -> List[str]:
        """
        Scans the source directory for files.
        Returns a list of absolute file paths.
        """
        files_found = []
        try:
            for entry in os.scandir(self.source_dir):
                if entry.is_file():
                    files_found.append(entry.path)
            logger.info(f"Docs found in {self.source_dir}: {len(files_found)}")
        except Exception as e:
            logger.error(f"Error scanning source dir: {e}")
        
        return files_found

    def move_to_stage(self, file_path: str, stage_dir: str) -> str:
        """
        Moves a file from source to stage for processing.
        Returns the new path in stage.
        """
        if not os.path.exists(stage_dir):
            os.makedirs(stage_dir)
            
        filename = os.path.basename(file_path)
        dest_path = os.path.join(stage_dir, filename)
        
        try:
            shutil.move(file_path, dest_path)
            logger.info(f"Moved {filename} to staging.")
            return dest_path
        except Exception as e:
            logger.error(f"Failed to move {filename}: {e}")
            raise
