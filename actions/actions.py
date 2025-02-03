import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Load lightweight model (80MB RAM)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Memory-mapped FAISS index (reduces RAM usage by 50%)
index = faiss.read_index("data/error_index.faiss", faiss.MMAP)

# Load error codes
df = pd.read_csv("data/errors.csv")

class ActionFetchSolution(Action):
    def name(self) -> str:
        return "action_fetch_solution"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_query = tracker.latest_message.get("text")
        query_embed = model.encode([user_query])
        distances, indices = index.search(query_embed, 1)
        error_code = df.iloc[indices[0][0]]["error_code"]
        solution = df[df["error_code"] == error_code]["description"].values[0]
        dispatcher.utter_message(text=f"**{error_code}**: {solution}")
        return []
