# src/textSummarizer/pipeline/stage_01_data_ingestion.py

from textSummarizer.config.configuration import ConfigurationManager
from textSummarizer.components.data_ingestion import DataIngestion
from textSummarizer.logging import logger

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        """
        This is the main method for the data ingestion pipeline.
        It orchestrates the entire data ingestion process.
        """
        logger.info("Starting Data Ingestion stage...")
        try:
            # Initialize the configuration manager
            config = ConfigurationManager()
            
            # Get the data ingestion configuration
            data_ingestion_config = config.get_data_ingestion_config()
            
            # Create the DataIngestion component
            data_ingestion = DataIngestion(config=data_ingestion_config)
            
            # Execute the steps
            logger.info("Downloading data...")
            data_ingestion.download_file()
            
            logger.info("Extracting data...")
            data_ingestion.extract_zip_file()
            
            logger.info("Data Ingestion stage completed successfully.\n\n")

        except Exception as e:
            logger.error(f"Data Ingestion stage failed: {e}")
            raise e