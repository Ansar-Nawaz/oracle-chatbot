import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from functools import lru_cache

# Load data and models
df = pd.read_csv('/home/orasniper/oracle-chatbot/data/oracle_errors.csv')
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index('/home/orasniper/oracle-chatbot/models/oracle_errors.index')

@lru_cache(maxsize=1000)  # Cache frequent queries
def get_answer(user_query: str) -> str:
    # Convert query to embedding
    query_embedding = model.encode([user_query], convert_to_numpy=True)
    
    # Search FAISS index
    distances, indices = index.search(query_embedding, k=1)
    closest_error = df.iloc[indices[0][0]]
    
    return f"""
    **Error**: {closest_error['code']}
    **Description**: {closest_error['description']}
    **Cause**: {closest_error['cause']}
    **Solution**: {closest_error['solution']}
    """

# Example usage:
print(get_answer("How to fix ORA-00904?"))


