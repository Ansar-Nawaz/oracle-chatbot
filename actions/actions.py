from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("data/error_index.faiss")
df = pd.read_csv("data/errors.csv")

class ActionFetchSolution(Action):
    def name(self) -> Text:
        return "action_fetch_solution"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict):
        user_query = tracker.latest_message.get("text")
        query_embed = model.encode([user_query])
        _, indices = index.search(query_embed, 1)
        error_code = df.iloc[indices[0][0]]["error_code"]
        solution = df[df["error_code"] == error_code]["description"].values[0]
        dispatcher.utter_message(text=f"**{error_code}**: {solution}")
        dispatcher.utter_message(response="utter_ask_feedback")
        return []

class ActionStoreFeedback(Action):
    def name(self) -> Text:
        return "action_store_feedback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict):
        feedback = tracker.get_slot("feedback")
        # Store feedback in PostgreSQL (example)
        dispatcher.utter_message(response="utter_thanks")
        return []
