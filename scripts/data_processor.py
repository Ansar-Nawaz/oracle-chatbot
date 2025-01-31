import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load data
df = pd.read_csv('/home/orasniper/oracle-chatbot/data/oracle_errors.csv')
texts = df.apply(
    lambda row: f"Code: {row['code']}, Description: {row['description']}, Cause: {row['cause']}, Solution: {row['solution']}",
    axis=1
).tolist()

# Generate embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight and fast
embeddings = model.encode(texts, convert_to_numpy=True)
np.save('../data/embeddings.npy', embeddings)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
faiss.write_index(index, '/home/orasniper/oracle-chatbot/models/oracle_errors.index')

