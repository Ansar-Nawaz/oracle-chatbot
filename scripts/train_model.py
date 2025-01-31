import pandas as pd
from sentence_transformers import InputExample, losses, SentenceTransformer
from torch.utils.data import DataLoader

def train_model():
    df = pd.read_csv('/home/orasniper/oracle-chatbot/data/oracle_errors.csv')
    
    # Create training pairs
    train_examples = []
    for _, row in df.iterrows():
        train_examples.append(InputExample(
            texts=[row['description'], row['solution']],
            label=1.0
        ))
        # Add negative examples
        train_examples.append(InputExample(
            texts=[row['description'], "Unrelated error solution"],
            label=0.0
        ))

    # Initialize model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=32)
    train_loss = losses.CosineSimilarityLoss(model)

    # Fine-tune
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=3,
        warmup_steps=100
    )
    
    model.save('/home/orasniper/oracle-chatbot/models/finetuned_model')

