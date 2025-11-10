# make_model.py
import pandas as pd
import joblib
from collections import defaultdict

class SimpleRecommender:
    """
    아주 단순한 추천기:
    1) 전체 로그에서 아이템별 인기순위를 만든다.
    2) 특정 유저가 이미 본 아이템은 제외한다.
    3) 남은 것 중 인기 높은 것부터 k개 반환한다.
    """
    def __init__(self, interactions: pd.DataFrame):
        """
        interactions: user_id, item_id 컬럼을 가진 DataFrame
        """
        self.interactions = interactions

        # 1) 아이템 인기 계산
        item_counts = (
            interactions.groupby("item_id")["user_id"]
            .count()
            .sort_values(ascending=False)
        )
        self.item_popularity = item_counts.index.tolist()  # 인기순 item 리스트

        # 2) 유저별 시청(이용) 아이템 dict
        user_items = defaultdict(set)
        for row in interactions.itertuples(index=False):
            user_items[row.user_id].add(row.item_id)
        self.user_items = user_items

    def recommend(self, user_id: str, k: int = 5):
        """
        user_id가 아직 안 본 아이템 중에서 인기 높은 것부터 k개 추천
        """
        seen = self.user_items.get(user_id, set())
        recs = []
        for item in self.item_popularity:
            if item not in seen:
                recs.append(item)
            if len(recs) >= k:
                break
        return recs

def build_dummy_data():
    """
    실제론 DB나 CSV에서 읽겠지만,
    여기선 더미로 user-item 로그를 만든다.
    """
    data = [
        # user1은 A,B,C 봤다
        ("user1", "item_A"),
        ("user1", "item_B"),
        ("user1", "item_C"),

        # user2는 A,C,D
        ("user2", "item_A"),
        ("user2", "item_C"),
        ("user2", "item_D"),

        # user3는 B,D,E
        ("user3", "item_B"),
        ("user3", "item_D"),
        ("user3", "item_E"),

        # user4는 A,E,F
        ("user4", "item_A"),
        ("user4", "item_E"),
        ("user4", "item_F"),

        # user5는 A,B
        ("user5", "item_A"),
        ("user5", "item_B"),
    ]
    df = pd.DataFrame(data, columns=["user_id", "item_id"])
    return df

if __name__ == "__main__":
    # 1) 더미 로그 만들기
    interactions = build_dummy_data()

    # 2) 추천기 학습(이라 쓰고 세팅이라 읽는다)
    model = SimpleRecommender(interactions)

    # 3) 테스트 한 번
    print("user1에게 추천:", model.recommend("user1", k=5))
    print("신규유저에게 추천:", model.recommend("new_user", k=5))

    # 4) 저장
    joblib.dump(model, "model.pkl")
    print("model.pkl 저장 완료")