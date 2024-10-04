from transformers import BertTokenizer, BertForSequenceClassification
import torch
import webbrowser
from stt import main as stt_main

# Function to load model and tokenizer
def load_model_and_tokenizer(model_path="./fine-tuned-parsbert", tokenizer_name="HooshvareLab/bert-fa-base-uncased"):
    try:
        model = BertForSequenceClassification.from_pretrained(model_path)
        tokenizer = BertTokenizer.from_pretrained(tokenizer_name)
        return model, tokenizer
    except Exception as e:
        print(f"Error loading model or tokenizer: {e}")
        return None, None


# Function to make a prediction on a given sentence
def predict_category(sentence, model, tokenizer):
    inputs = tokenizer(sentence, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=-1).item()

    # Map predicted class to product category
    product_categories = {0: "Electronic Devices", 1: "Groceries", 2: "Clothing", 3: "Furniture", 4: "Books"}
    return product_categories.get(predicted_class, "Unknown")


# Function to open Google search for a query
def open_google_search(query):
    query = query.replace(" ", "+")  # Format query for URL
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)  # Open the URL in the default web browser


# Main function
def main():

    sentence = stt_main() # Example Persian sentence

    # Load the model and tokenizer
    model, tokenizer = load_model_and_tokenizer()
    if model is None or tokenizer is None:
        return

    # Predict the category
    predicted_category = predict_category(sentence, model, tokenizer)
    print(f"The sentence '{sentence}' is related to the category: {predicted_category}")

    # If predicted category is 'Groceries', open Google search
    if predicted_category.lower() == "groceries":
        open_google_search(sentence)  # Use sentence directly for search query


if __name__ == "__main__":
    main()
