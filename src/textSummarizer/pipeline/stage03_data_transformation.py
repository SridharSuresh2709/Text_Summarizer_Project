# src/textSummarizer/pipeline/stage_03_data_transformation.py

from textSummarizer.config.configuration import ConfigurationManager
from textSummarizer.components.data_transformation import DataTransformation
from textSummarizer.logging import logger

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        logger.info("Starting Data Transformation stage...")
        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(config=data_transformation_config)
            data_transformation.convert()
            logger.info("Data Transformation stage completed successfully.\n\n")
        except Exception as e:
            logger.error(f"Data Transformation stage failed: {e}")
            raise e