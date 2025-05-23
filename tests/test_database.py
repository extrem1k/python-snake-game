import pytest
from database.models import (
    create_user,
    get_user,
    update_user,
    delete_user,
    create_score,
    get_scores_by_user,
    update_score,
    delete_score,
)
from bson import ObjectId

# ====== TESTY DLA USERS ======


def test_user_crud():
    # CREATE
    nickname = "test_user"
    user_id = create_user(nickname)
    assert isinstance(user_id, ObjectId)

    # READ
    user_data = get_user(user_id)
    assert user_data is not None
    assert user_data["nickname"] == nickname

    # UPDATE
    new_nickname = "updated_user"
    update_count = update_user(user_id, {"nickname": new_nickname})
    assert update_count == 1

    updated_user = get_user(user_id)
    assert updated_user["nickname"] == new_nickname

    # DELETE
    delete_count = delete_user(user_id)
    assert delete_count == 1

    deleted_user = get_user(user_id)
    assert deleted_user is None


# ====== TESTY DLA SCORES ======


def test_score_crud():
    # Najpierw utwórz użytkownika, do którego przypiszemy score
    nickname = "score_user"
    user_id = create_user(nickname)

    # CREATE
    final_score = 10
    play_time = 45.0
    score_id = create_score(user_id, final_score, play_time)
    assert isinstance(score_id, ObjectId)

    # READ
    scores = get_scores_by_user(user_id)
    assert len(scores) >= 1
    score = [s for s in scores if s["_id"] == score_id][0]
    assert score["final_score"] == final_score

    # UPDATE
    update_count = update_score(score_id, {"final_score": 20})
    assert update_count == 1

    updated_scores = get_scores_by_user(user_id)
    updated_score = [s for s in updated_scores if s["_id"] == score_id][0]
    assert updated_score["final_score"] == 20

    # DELETE
    delete_count = delete_score(score_id)
    assert delete_count == 1

    remaining_scores = get_scores_by_user(user_id)
    assert all(s["_id"] != score_id for s in remaining_scores)

    # Usuń testowego użytkownika
    delete_user(user_id)
