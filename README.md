# Conversational Big 5

This project explores and implements a conversational interface for analyzing and interpreting personality traits based on the Big Five personality model. It enables users to engage in conversations and receive insights into personality characteristics such as openness, conscientiousness, extraversion, agreeableness, and neuroticism.

## Installation

Follow these steps to set up the project locally:

```bash
# Clone the repository
git clone https://github.com/kerwin145/conversational-big5.git

# Navigate to the project directory
cd conversational-big5

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Original Source
Ensure the `original source` is set to `null` before proceeding.

### 2. Data Generation
Use `data-gen.py` to generate data. This script uses AI-generated outputs to create answers to the questions in the training dataset:

```bash
python data-gen.py
```

### 3. Training the Model
Use `model_v2.ipynb` to train the model based on the BERT architecture. This notebook processes the training dataset and saves the trained model to the `model2` directory:

1. Open `model_v2.ipynb` in a Jupyter Notebook or a compatible environment.
2. Run the cells to train the model.
3. Ensure the trained model is saved to the `model2` directory.

### 4. Running the Interface
Use `interface.py` to interact with the trained model:

```bash
python interface.py
```

This script serves as the interface for using the trained model to analyze and interpret conversational input.

## Features

- **Personality Analysis**: Understand personality traits based on conversational input.
- **Interactive Interface**: Engage in a conversation-like experience for analysis.
- **Big Five Model**: Focuses on openness, conscientiousness, extraversion, agreeableness, and neuroticism.




