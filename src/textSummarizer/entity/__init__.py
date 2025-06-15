# src/textSummarizer/entity/__init__.py

from dataclasses import dataclass
from pathlib import Path

# This is a dataclass that defines the structure of the data ingestion configuration.
# Think of it as defining the "type" for our config variables.
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    ALL_REQUIRED_FILES: list

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    tokenizer_name: str

# NEW, CORRECTED ENTITY
@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    data_path: Path
    model_ckpt: str
    num_train_epochs: int
    warmup_steps: int
    per_device_train_batch_size: int
    weight_decay: float
    logging_steps: int
    do_eval: bool             # <-- USE THIS MODERN NAME
    save_steps: float
    gradient_accumulation_steps: int
    # Remove evaluation_strategy and eval_steps