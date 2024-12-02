import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from torch.nn.utils.rnn import pad_sequence

class Big5Classifier:
    def __init__(self, model_name='distilbert-base-uncased', num_classes=2):
        # Initialize models here
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels = num_classes)
    def get_tokenizer_and_model(self):
        return self.model, self.tokenizer  
    
class Interface:
    def __init__(self, model_paths, device="cpu"):
        self.models = {}
        self.tokenizers = {}
        self.device = device
        self.questionMap = {
            "Openness": "This is a question about openness: Describe a time when you tried something completely new—whether it was a different activity, way of thinking, or environment. What motivated you to try it, and how did you feel about the experience afterward?",
            "Conscientiousness": "This is a question about conscientiousness: Think of a goal you set for yourself that required sustained effort over time. How did you manage your time and resources to stay on track, and what strategies helped you stay committed, even when challenges came up? What did you find challenging or rewarding about the experience?",
            "Extraversion": "This is a question about extraversion: Recall a memorable social experience that either energized you or left you feeling drained. What do you think made the interaction fulfilling or draining? How did it shape your understanding of your social preferences or needs?",
            "Agreeableness": "This is a question about agreeableness: Describe a situation where you found yourself in disagreement with someone. How did you handle the situation, and what were your priorities in resolving or understanding the conflict?",
            "Neuroticism": "This is a question about neuroticism: Think of a time when you felt particularly stressed or anxious. How did you respond initially, and what steps did you take to manage your emotions and approach the situation constructively?"
        }
        self.load_models(model_paths)

    def load_models(self, model_paths):
        """
        Load each model and its tokenizer and store them in a dictionary.
        """
        for trait, model_path in model_paths.items():
            transformer = Big5Classifier(model_name=model_path)
            model, tokenizer = transformer.get_tokenizer_and_model()
            self.models[trait] = model.to(self.device)
            self.tokenizers[trait] = tokenizer

    def tokenize_input(self, trait, answer):
        """
        Tokenize the input using the specific tokenizer for the given trait.
        """
        tokenizer = self.tokenizers[trait]
        # encoded = tokenizer(
        #     f"{self.questionMap[trait]} [SEP] {answer}",
        #     max_length=400,
        #     truncation=True,
        #     padding="max_length",
        #     return_tensors="pt"
        # )
        encoded = tokenizer(
            answer,
            max_length=400,
            truncation=True,
            padding="max_length",
            return_tensors="pt"
        )
        input_ids = encoded["input_ids"].to(self.device)  # Token IDs
        attention_mask = encoded["attention_mask"].to(self.device)  # Attention mask
        return input_ids, attention_mask

    def predict(self, trait, input_ids, attention_mask):
        """
        Perform prediction for the given trait using the corresponding model.
        """
        model = self.models[trait]
        model.eval()
        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            pred = torch.argmax(probabilities, dim=1).item()
        return pred, probabilities[0].tolist()

    def ask_questions(self):
        """
        Interactively ask the user questions for each trait and provide predictions.
        """
        results = {}
        for trait in self.questionMap.keys():
            print(f"\n{self.questionMap[trait]}")
            answer = input("Your response: ")

            # Tokenize and predict
            input_ids, attention_mask = self.tokenize_input(trait, answer)
            prediction, probabilities = self.predict(trait, input_ids, attention_mask)

            # Display result
            result_text = "Yes" if prediction == 1 else "No"
            print(f"Prediction for {trait}: {result_text} (Confidence: {probabilities[prediction]:.2f})")
            results[trait] = {"Prediction": result_text, "Confidence": probabilities[prediction]}

        return results


# Define the paths to your trained models
model_paths = {
    "Openness": "models/Big5_OPN_top_4_training",
    "Conscientiousness": "models/Big5_CON_top_4_training",
    "Extraversion": "models/Big5_EXT_top_4_training",
    "Agreeableness": "models/Big5_AGR_top_4_training",
    "Neuroticism": "models/Big5_NEU_top_4_training"
}

# Run the interface
if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    interface = Interface(model_paths, device=device)
    print("Welcome to the Big 5 Personality Predictor!")
    results = interface.ask_questions()
    print("\nFinal Results:")
    for trait, result in results.items():
        print(f"{trait}: {result['Prediction']} (Confidence: {result['Confidence']:.2f})")
