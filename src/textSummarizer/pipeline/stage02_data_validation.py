# src/textSummarizer/pipeline/stage_02_data_validation.py

from textSummarizer.config.configuration import ConfigurationManager
from textSummarizer.components.data_validation import DataValidation
from textSummarizer.logging import logger

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        logger.info("Starting Data Validation stage...")
        try:
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValidation(config=data_validation_config)
            data_validation.validate_all_files_exist()
            logger.info("Data Validation stage completed successfully.\n\n")
        except Exception as e:
            logger.error(f"Data Validation stage failed: {e}")
            raise e