import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def generate_embeddings():
    df = pd.read_csv('/home/orasniper/oracle-chatbot/data/oracle_errors.csv')
    
    # Structured context format
    texts = df.apply(lambda row: f"""
    Oracle Error Code: {row['code']}
    Error Context: {row['description']}
    Typical Causes: {row['cause']}
    Recommended Fixes: {row['solution']}
    """, axis=1).tolist()

    # Load fine-tuned model
    model = SentenceTransformer('/home/orasniper/oracle-chatbot/models/finetuned_model')
    embeddings = model.encode(texts, convert_to_numpy=True)
    np.save('/home/orasniper/oracle-chatbot/data/embeddings.npy', embeddings)

    # Quantized FAISS index
    dimension = embeddings.shape[1]
    quantizer = faiss.IndexFlatL2(dimension)
    index = faiss.IndexIVFPQ(quantizer, dimension, 100, 16, 8)
    index.train(embeddings)
    index.add(embeddings)
    faiss.write_index(index, '/home/orasniper/oracle-chatbot/models/oracle_errors.index')

