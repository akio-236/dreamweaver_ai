import os
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    TextDataset,
    DataCollatorForLanguageModeling,
)
import torch

MODEL_NAME = "distilgpt2"
DATA_FILE_PATH = "data/processed_stories/combined_children_stories.txt"
OUTPUT_DIR = "./llm_fine_tuned_model"
LOGGING_DIR = "./llm_fine_tuned_model/logs"
BATCH_SIZE = 2
GRADIENT_ACCUMULATION_STEPS = 4
BLOCK_SIZE = 128
NUM_TRAIN_EPOCHS = 3

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOGGING_DIR, exist_ok=True)

print(f"Loading tokenizer and model: {MODEL_NAME}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print(f"Loading dataset from: {DATA_FILE_PATH}")

train_dataset = TextDataset(
    tokenizer=tokenizer, file_path=DATA_FILE_PATH, block_size=BLOCK_SIZE
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

print("Configuring training arguments...")
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,
    num_train_epochs=NUM_TRAIN_EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
    save_steps=10_000,
    save_total_limit=2,
    logging_dir=LOGGING_DIR,
    logging_steps=500,
    learning_rate=5e-5,
    weight_decay=0.01,
    fp16=torch.cuda.is_available(),
    remove_unused_columns=False,
)


print("Initializing Trainer...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=data_collator,
)

print("Starting fine tuning...")
try:
    trainer.train()
    print("Fine tuning completed successfully!.")

    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"Fine tuned model and tokenizer saved to {OUTPUT_DIR}.")
except torch.cuda.OutOfMemoryError:
    print(
        "CUDA Out of Memory! Try reducing BATCH_SIZE or BLOCK_SIZE, or increasing GRADIENT_ACCUMULATION_STEPS."
    )
except Exception as e:
    print(f"An error occurred during training: {e}")
