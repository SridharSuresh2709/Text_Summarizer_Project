# src/textSummarizer/pipeline/stage_04_model_trainer.py

from textSummarizer.config.configuration import ConfigurationManager
from textSummarizer.components.model_trainer import ModelTrainer
from textSummarizer.logging import logger

class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        logger.info("Starting Model Training stage...")
        try:
            config = ConfigurationManager()
            model_trainer_config = config.get_model_trainer_config()
            model_trainer = ModelTrainer(config=model_trainer_config)
            model_trainer.train()
            logger.info("Model Training stage completed successfully.\n\n")
        except Exception as e:
            logger.error(f"Model Training stage failed: {e}")
            raise e