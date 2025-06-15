# src/textSummarizer/components/data_transformation.py

from transformers import AutoTokenizer
from datasets import load_dataset
from textSummarizer.entity import DataTransformationConfig
from textSummarizer.logging import logger
import os

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)

    # This method is part of the class
    def convert_examples_to_features(self, example_batch):
        input_encodings = self.tokenizer(example_batch['dialogue'], max_length=1024, truncation=True)

        with self.tokenizer.as_target_tokenizer():
            target_encodings = self.tokenizer(example_batch['summary'], max_length=128, truncation=True)

        return {
            'input_ids': input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': target_encodings['input_ids']
        }

    # This 'convert' method must also be indented to be part of the class
    def convert(self):
        logger.info("Loading data from CSV files...")
        raw_dataset = load_dataset('csv', data_files={'train': 'artifacts/data_ingestion/samsum-train.csv',
                                                      'test': 'artifacts/data_ingestion/samsum-test.csv',
                                                      'validation': 'artifacts/data_ingestion/samsum-validation.csv'})

        logger.info("Filtering out rows with missing 'dialogue' or 'summary'...")

        # --- IMPORTANT: 'filter_nones' is defined INSIDE 'convert' ---
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