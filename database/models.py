from datetime import datetime

from database.db import get_database

db = get_database()


users_collection = db["users"]
scores_collection = db["scores"]


def create_user(nickname, score=0):
    user_data = {"nickname": nickname, "score": score, "created_at": datetime.utcnow()}
    result = users_collection.insert_one(user_data)
    return result.inserted_id


def get_user(user_id):
    return users_collection.find_one({"_id": user_id})


def update_user(user_id, update_fields: dict):
    result = users_collection.update_one({"_id": user_id}, {"$set": update_fields})
    return result.modified_count


def delete_user(user_id):
    result = users_collection.delete_one({"_id": user_id})
    return result.deleted_count


# ===== Operacje CRUD dla wyników gier =====


def create_score(user_id, final_score, play_time):
    score_data = {
        "user_id": user_id,
        "final_score": final_score,
        "play_time": play_time,
        "date": datetime.utcnow(),
    }
    result = scores_collection.insert_one(score_data)
    return result.inserted_id


def get_scores_by_user(user_id):
    return list(scores_collection.find({"user_id": user_id}))


def update_score(score_id, update_fields: dict):
    result = scores_collection.update_one({"_id": score_id}, {"$set": update_fields})
    return result.modified_count


def save_score(user_id, board_size, score, nickname):
    document = {
        "user_id": user_id,
        "nickname": nickname,
        "board_size": board_size,
        "score": score,
        "timestamp": datetime.now(),
    }
    scores_collection.insert_one(document)


def delete_score(score_id):
    result = scores_collection.delete_one({"_id": score_id})
    return result.deleted_count
