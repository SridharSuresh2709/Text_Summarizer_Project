# src/textSummarizer/components/data_transformation.py

from transformers import AutoTokenizer
from datasets import Dataset, DatasetDict
from textSummarizer.entity import DataTransformationConfig
from textSummarizer.logging import logger
import os
import pandas as pd

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)

    def convert_examples_to_features(self, example_batch):
        input_encodings = self.tokenizer(example_batch['dialogue'], max_length=1024, truncation=True)

        with self.tokenizer.as_target_tokenizer():
            target_encodings = self.tokenizer(example_batch['summary'], max_length=128, truncation=True)

        return {
            'input_ids': input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': target_encodings['input_ids']
        }

    def convert(self):
        # --- THIS IS THE NEW, CORRECTED LOGIC ---
        logger.info("Loading data from local CSV files...")
        
        # Define paths to the CSV files
        train_path = os.path.join(self.config.data_path, "samsum-train.csv")
        test_path = os.path.join(self.config.data_path, "samsum-test.csv")
        validation_path = os.path.join(self.config.data_path, "samsum-validation.csv")
        
        # Load CSVs into pandas DataFrames
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)
        df_validation = pd.read_csv(validation_path)
        
        # Create Dataset objects from pandas DataFrames
        train_dataset = Dataset.from_pandas(df_train)
        test_dataset = Dataset.from_pandas(df_test)
        validation_dataset = Dataset.from_pandas(df_validation)
        
        # Combine them into a single DatasetDict object
        raw_dataset = DatasetDict({
            'train': train_dataset,
            'test': test_dataset,
            'validation': validation_dataset
        })
        # --- END OF NEW LOGIC ---

        logger.info("Filtering out rows with missing 'dialogue' or 'summary'...")
        
        def filter_nones(example):
            return example['dialogue'] is not None and example['summary'] is not None
        
        cleaned_dataset = raw_dataset.filter(filter_nones)
        
        logger.info(f"Original train size: {len(raw_dataset['train'])}. Cleaned train size: {len(cleaned_dataset['train'])}")

        logger.info("Applying tokenization and converting to features...")
        tokenized_dataset = cleaned_dataset.map(self.convert_examples_to_features, batched=True,
                                                remove_columns=cleaned_dataset["train"].column_names)

        output_path = os.path.join(self.config.root_dir, "samsum_dataset_tokenized")
        logger.info(f"Saving tokenized data to {output_path}...")
        tokenized_dataset.save_to_disk(output_path)
        
        logger.info("Data transformation complete.")