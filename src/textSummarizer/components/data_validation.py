# src/textSummarizer/components/data_validation.py

import os
from textSummarizer.logging import logger
from textSummarizer.entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_files_exist(self)-> bool:
        """
        Validates that all required files exist in the data ingestion directory.
        Writes the validation status to a file.
        Returns True if all files exist, False otherwise.
        """
        try:
            validation_status = None

            # Get the list of all files in the data ingestion directory
            all_files = os.listdir(os.path.join("artifacts","data_ingestion"))

            # Check if each required file is in the list of all files
            for file in self.config.ALL_REQUIRED_FILES:
                if file not in all_files:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                    logger.warning(f"Validation failed: {file} is missing.")
                    return validation_status
                
            # If the loop completes, all files were found
            validation_status = True
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")
            logger.info("Validation successful. All required files exist.")
            return validation_status

        except Exception as e:
            logger.error(f"Error during file validation: {e}")
            raise e