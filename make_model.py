# make_model.py
import joblib
from recommender import SimpleRecommender, build_dummy_data

if __name__ == "__main__":
    interactions = build_dummy_data()
    model = SimpleRecommender(interactions)
    joblib.dump(model, "model.pkl")
    print("saved model.pkl")