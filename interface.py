import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

def load_model(model_path, model_name):
    print(f"Loading model for {model_name} from {model_path}...")
    
    # check if all necessary files are in the path
    required_files = [
        "model.safetensors", "vocab.txt", "special_tokens_map.json",
        "tokenizer_config.json", "config.json", "tokenizer.json"
    ]
    
    for file in required_files:
        file_path = os.path.join(model_path, file)
        if not os.path.exists(file_path):
            raise ValueError(f"Missing necessary file: {file} in the directory for {model_name} at {model_path}")
    
    # Load the model and tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=2)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    return model, tokenizer


# Main function to run the personality test
def main():
    print("Welcome to the Big-5 Personality Test!")
    print("Please answer each question honestly.\n")
    
    # model paths for each personality trait
    model_paths = {
        "Openness": "models/Big5_OPN_top_4_training",
        "Conscientiousness": "models/Big5_CON_top_4_training",
        "Extraversion": "models/Big5_EXT_top_4_training",
        "Agreeableness": "models/Big5_AGR_top_4_training",
        "Neuroticism": "models/Big5_NEU_top_4_training"
    }

    # Load models for each trait
    models = {}
    for trait, path in model_paths.items():
        try:
            model, tokenizer = load_model(path, trait)
            models[trait] = (model, tokenizer)
            print(f"{trait} model loaded successfully!")
        except ValueError as e:
            print(e)

    #questions for the Big-5 Personality Test
    questions = {
        "Openness": "Describe a time when you tried something completely new. What motivated you, and how did you feel afterward? ",
        "Conscientiousness": "Think of a goal you set for yourself that required sustained effort over time. How did you manage it? ",
        "Extraversion": "Recall a memorable social experience that either energized you or drained you. What made it fulfilling or draining? ",
        "Agreeableness": "Describe a situation where you disagreed with someone. How did you handle it? ",
        "Neuroticism": "Think of a time when you felt particularly stressed or anxious. How did you respond initially, and how did you manage it? "
    }

    responses = {}  # store user responses for each trait
    for trait, question in questions.items():
        print(f"{trait}: {question}")
        response = input("Your answer: ")
        responses[trait] = response

    results = []
    for trait, response in responses.items():
        
        model, tokenizer = models[trait]
        
        # tokenize the response for this trait 
        # inputs = tokenizer(response, return_tensors="pt", padding=True, truncation=True)
        
        qa_concat = f"This is a question about {trait}: {questions[trait]} [SEP] {response}"
        print(qa_concat)
        encoded_inputs = tokenizer(
            qa_concat,
            return_tensors="pt",  # Return PyTorch tensors
            max_length=400,
            truncation=True,
            padding=True
        )    

        device = next(model.parameters()).device
        encoded_inputs = {key: value.to(device) for key, value in encoded_inputs.items()}
        
        # Get the outputs from the model
        outputs = model(**encoded_inputs)
        
        # Use softmax to convert logits to probabilities
        softmax_probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(softmax_probs, dim=-1)
        
        # probabilities
        no_prob = softmax_probs[0][0].item()  # Probability for class 0 (No)
        yes_prob = softmax_probs[0][1].item()  # Probability for class 1 (Yes)

        # Decide Y/N based on the predicted class
        prediction = 'y' if predicted_class.item() == 1 else 'n'
        results.append(prediction)
        print(f"Prediction for {trait}: {prediction}")
        print(f"Probability for No: {no_prob:.4f}, Probability for Yes: {yes_prob:.4f}")
        

    # Final result as a vector
    final_result = ",".join(results)
    print(f"Final Result: {final_result}")


if __name__ == "__main__":
    main()