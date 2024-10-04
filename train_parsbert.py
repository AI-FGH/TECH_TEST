
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
import torch

# Load dataset (assuming you have two CSV files: one for training and one for testing)
train_dataset = load_dataset("csv", data_files="product_data_train.csv")["train"] # Change to your training CSV file
test_dataset = load_dataset("csv", data_files="product_data_test.csv")["train"]   # Change to your testing CSV file

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("HooshvareLab/bert-fa-base-uncased")

# Define tokenization function
def tokenize_function(examples):
    tokenized_inputs = tokenizer(examples["content"], padding="max_length", truncation=True)
    tokenized_inputs["labels"] = examples["label_id"]  # Use the correct label column
    return tokenized_inputs

# Apply tokenization
tokenized_train_dataset = train_dataset.map(tokenize_function, batched=False)
tokenized_test_dataset = test_dataset.map(tokenize_function, batched=False)

# Load model
model = AutoModelForSequenceClassification.from_pretrained("HooshvareLab/bert-fa-base-uncased", num_labels=2)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
)

# Define trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_test_dataset,  # Use the test dataset for evaluation
)

# Train model
trainer.train()
model.save_pretrained("./fine-tuned-parsbert")
tokenizer.save_pretrained("./fine-tuned-parsbert")


