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

    # This 'convert' method is also part of the class
    def convert(self):
        # THE ONLY CHANGE IS HERE:
        logger.info("Loading data from the Hugging Face Hub cache...")
        # We load by its name 'samsum', which is passed from the config file.
        # This will use the already-downloaded version from the cache.
        raw_dataset = load_dataset(self.config.data_path)

        # ALL OF YOUR CUSTOM LOGIC BELOW REMAINS UNCHANGED
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