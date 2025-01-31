import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from collections import deque
from functools import lru_cache

class ChatSession:
    def __init__(self, session_id, max_history=3):
        self.session_id = session_id
        self.history = deque(maxlen=max_history)
        self.df = pd.read_csv('/home/orasniper/oracle-chatbot/data/oracle_errors.csv')
        self.model = SentenceTransformer('/home/orasniper/oracle-chatbot/models/finetuned_model')
        self.index = faiss.read_index('/home/orasniper/oracle-chatbot/models/oracle_errors.index')
    
    def _format_context(self):
        return "\n".join([f"Q: {q}\nA: {a}" for q, a in self.history])
    
    @lru_cache(maxsize=1000)
    def _search_index(self, query):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, 3)
        return [self.df.iloc[i] for i in indices[0]]

    def ask(self, query):
        contextual_query = f"""
        Conversation History:
        {self._format_context()}
        New Query: {query}
        """
        
        results = self._search_index(contextual_query)
        best_match = results[0]
        
        self.history.append((query, best_match['solution']))
        return {
            'code': best_match['code'],
            'description': best_match['description'],
            'cause': best_match['cause'],
            'solution': best_match['solution'],
            'confidence': results[0]['score']
        }

