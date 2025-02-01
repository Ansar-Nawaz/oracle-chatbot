from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

os.environ["PORT"] = "5005"
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("data/error_index.faiss")
df = pd.read_csv("data/errors.csv")

class ActionFetchSolution(Action):
    def name(self):
        return "action_fetch_solution"

    def run(self, dispatcher, tracker, domain):
        user_query = tracker.latest_message.get('text')
        query_embed = model.encode([user_query])
        _, indices = index.search(query_embed, 1)
        error_code = df.iloc[indices[0][0]]['error_code']
        solution = df[df['error_code'] == error_code]['description'].values[0]
        dispatcher.utter_message(text=f"**{error_code}**: {solution}")
        return []
