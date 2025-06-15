from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_from_disk
from textSummarizer.entity import ModelTrainerConfig
import torch
import os

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
        
        # --- THE DEFINITIVE FIX ---
        # Get the absolute path
        abs_path = os.path.abspath(self.config.data_path)
        
        # Prepend the 'file://' protocol to create a URI
        # This explicitly tells the 'datasets' library to use the local file system
        data_path_uri = f"file://{abs_path}"
        
        print(f"Loading dataset from URI: {data_path_uri}") # For debugging
        dataset_samsum_pt = load_from_disk(data_path_uri)
        # --- END OF FIX ---

        # This is the corrected version for TrainingArguments
        trainer_args = TrainingArguments(
        output_dir=self.config.root_dir, 
        num_train_epochs=self.config.num_train_epochs, 
        warmup_steps=self.config.warmup_steps,
        per_device_train_batch_size=self.config.per_device_train_batch_size, 
        weight_decay=self.config.weight_decay,
        logging_steps=self.config.logging_steps,
        do_eval=self.config.do_eval, # <-- USE THIS MODERN NAME
        save_steps=self.config.save_steps,
        gradient_accumulation_steps=self.config.gradient_accumulation_steps,
        # The 'evaluation_strategy' will be set automatically based on 'do_eval'
        # The 'eval_steps' parameter can be set here if needed, but the default is often fine.
        # For simplicity, we'll let the Trainer use its defaults for evaluation timing.
    )
        trainer = Trainer(model=model, args=trainer_args,
                          tokenizer=tokenizer, data_collator=seq2seq_data_collator,
                          train_dataset=dataset_samsum_pt["train"], 
                          eval_dataset=dataset_samsum_pt["validation"])
        
        trainer.train()

        # Save model
        model.save_pretrained(os.path.join(self.config.root_dir,"pegasus-samsum-model"))
        # Save tokenizer
        tokenizer.save_pretrained(os.path.join(self.config.root_dir,"pegasus-samsum-tokenizer"))