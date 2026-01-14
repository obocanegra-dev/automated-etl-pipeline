import sys
import os
import logging
import shutil
import time

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("pipeline.log")
    ]
)
logger = logging.getLogger("ETL_Pipeline")

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import load_config
from extractor import FileExtractor
from validator import FileValidator
from cloud_connector import CloudConnectorFactory
from sftp_connector import SFTPConnector

def main():
    logger.info("Starting ETL Pipeline...")

    # 1. Load Config
    try:
        config = load_config()
        logger.info(f"Configuration loaded. Env: {config.environment}")
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return

    # 2. Initialize Components
    extractor = FileExtractor(config.paths.source)
    validator = FileValidator()
    
    # Connectors
    try:
        s3_provider = CloudConnectorFactory.get_provider(config, 'aws')
        azure_provider = CloudConnectorFactory.get_provider(config, 'azure')
        sftp_provider = SFTPConnector(
            config.sftp['host'], 
            config.sftp['port'], 
            config.sftp['username'], 
            config.sftp['password'], 
            config.sftp['remote_path']
        )
    except Exception as e:
        logger.error(f"Failed to initialize connectors: {e}")
        return

    # 3. Operations Loop (Single run for now, could be a while loop)
    files = extractor.scan_for_files()
    
    for file_path in files:
        filename = os.path.basename(file_path)
        logger.info(f"Processing: {filename}")

        # VALIDATION
        is_valid, normalized_name, error_reason = validator.normalize(filename)
        
        if not is_valid:
            logger.warning(f"Validation FAILED: {filename} -> {error_reason}")
            # Move to error
            shutil.move(file_path, os.path.join(config.paths.error, filename))
            continue
        
        logger.info(f"Validation PASSED. Normalized: {normalized_name}")
        
        # STAGING
        try:
            staged_path = extractor.move_to_stage(file_path, config.paths.stage)
        except Exception as e:
            logger.error(f"Staging failed for {filename}: {e}")
            continue

        # LOAD (Cloud & SFTP)
        success_count = 0
        
        # AWS
        if s3_provider.upload_file(staged_path, normalized_name):
            success_count += 1
            
        # Azure
        if azure_provider.upload_file(staged_path, normalized_name):
            success_count += 1
            
        # SFTP
        if sftp_provider.upload(staged_path):
            success_count += 1

        # ARCHIVE (if at least one upload succeeded)
        if success_count > 0:
            shutil.move(staged_path, os.path.join(config.paths.archive, normalized_name))
            logger.info(f"Archived {normalized_name}")
        else:
            logger.error(f"Failed to upload {normalized_name} to any destination.")

    logger.info("ETL Pipeline Run Complete.")

if __name__ == "__main__":
    main()
