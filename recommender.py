# recommender.py
import pandas as pd
from collections import defaultdict

class SimpleRecommender:
    def __init__(self, interactions: pd.DataFrame):
        item_counts = (
            interactions.groupby("item_id")["user_id"]
            .count()
            .sort_values(ascending=False)
        )
        self.item_popularity = item_counts.index.tolist()

        user_items = defaultdict(set)
        for row in interactions.itertuples(index=False):
            user_items[row.user_id].add(row.item_id)
        self.user_items = user_items

    def recommend(self, user_id: str, k: int = 5):
        seen = self.user_items.get(user_id, set())
        recs = []
        for item in self.item_popularity:
            if item not in seen:
                recs.append(item)
            if len(recs) >= k:
                break
        return recs

def build_dummy_data():
    data = [
        ("user1", "item_A"),
        ("user1", "item_B"),
        ("user1", "item_C"),
        ("user2", "item_A"),
        ("user2", "item_C"),
        ("user2", "item_D"),
        ("user3", "item_B"),
        ("user3", "item_D"),
        ("user3", "item_E"),
        ("user4", "item_A"),
        ("user4", "item_E"),
        ("user4", "item_F"),
        ("user5", "item_A"),
        ("user5", "item_B"),
    ]
    df = pd.DataFrame(data, columns=["user_id", "item_id"])
    return df