from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd

df = pd.read_csv("data/errors.csv")
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(df["description"].tolist())

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
faiss.write_index(index, "data/error_index.faiss")
