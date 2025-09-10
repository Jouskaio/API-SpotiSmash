from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db_session
from app.infrastructure.database.orm import UserORM, TrackORM
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_user_tag_vector(user: UserORM, session: Session) -> Counter:
    tags = Counter()
    for playlist in user.playlists:
        for track in playlist.tracks:
            for tag in track.tags:
                tags[tag.name] += 1
    return tags

def vectorize(counter: Counter, tag_index: dict) -> np.ndarray:
    vector = np.zeros(len(tag_index))
    for tag, count in counter.items():
        idx = tag_index.get(tag)
        if idx is not None:
            vector[idx] = count
    return vector

def find_soulmate(user_id: str) -> str:
    with get_db_session() as session:
        all_users = session.query(UserORM).all()
        target_user = session.get(UserORM, user_id)

        if not target_user:
            raise ValueError("User not found")

        user_vectors = {}
        all_tags = set()

        for user in all_users:
            tag_counter = get_user_tag_vector(user, session)
            user_vectors[user.id] = tag_counter
            all_tags.update(tag_counter.keys())

        tag_index = {tag: i for i, tag in enumerate(sorted(all_tags))}

        target_vec = vectorize(user_vectors[target_user.id], tag_index)

        max_score = -1
        best_match = None

        for other_id, other_vec in user_vectors.items():
            if other_id == user_id:
                continue
            vec = vectorize(other_vec, tag_index)
            sim = cosine_similarity([target_vec], [vec])[0][0]
            if sim > max_score:
                max_score = sim
                best_match = other_id

        return best_match