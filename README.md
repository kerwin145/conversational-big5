# Conversational Big 5

This project explores and implements a conversational interface for analyzing and interpreting personality traits based on the Big Five personality model. It enables users to engage in a "conversation" and receive insights into personality characteristics such as openness, conscientiousness, extraversion, agreeableness, and neuroticism.

## Installation

Follow these steps to set up the project locally:

```bash
# Clone the repository
git clone https://github.com/kerwin145/conversational-big5.git

# Navigate to the project directory
cd conversational-big5

# Install dependencies as needed
```

## Usage

### 1. Data Generation
Use `data-gen.py` to generate data. This script uses AI-generated outputs to create answers to the questions in the training dataset:

```bash
python data-gen.py
```

### 2 Training the Model
Use `model_v2.ipynb` to train the model based on the BERT architecture. This notebook processes the training dataset and saves the trained model to the `model2` directory:
-  model.ipynb differs from model_v2.ipynb only in the dataset loader part, where we choose to concatenate the question to the answers for the model input.

1. Open `model_v2.ipynb` in a Jupyter Notebook or a compatible environment.
2. Run the cells to train the model.
3. Ensure the trained model is saved to the `model2` directory.

### 4. Running the Interface
Use `test_nterface.py` to interact with the trained model:

```bash
python test_interface.py
```

This script serves as the interface for using the trained model to analyze and interpret conversational input.

## Features

- **Personality Analysis**: Understand personality traits based on conversational input.
- **Interactive Interface**: Engage in a conversation-like experience for analysis.
- **Big Five Model**: Focuses on openness, conscientiousness, extraversion, agreeableness, and neuroticism.

### Here are the five questions asked from the model
- Openness to Experience: Describe a time when you tried something completely new—whether it was a different activity, way of thinking, or environment. What motivated you to try it, and how did you feel about the experience afterward?
- Conscientiousness: Think of a goal you set for yourself that required sustained effort over time. How did you manage your time and resources to stay on track, and what strategies helped you stay committed, even when challenges came up? What did you find challenging or rewarding about the experience?
- Extraversion: Recall a memorable social experience that either energized you or left you feeling drained. What do you think made the interaction fulfilling or draining? How did it shape your understanding of your social preferences or needs?
- Agreeableness: Describe a situation where you found yourself in disagreement with someone. How did you handle the situation, and what were your priorities in resolving or understanding the conflict?
- Neuroticism: Think of a time when you felt particularly stressed or anxious. How did you respond initially, and what steps did you take to manage your emotions and approach the situation constructively?




