from db import db

def get_reviews(addition_id):
    sql = """SELECT u.username, r.stars, r.comment, r.sent_at FROM reviews r, users u
    WHERE r.user_id=u.id AND r.addition_id=:addition_id ORDER BY r.sent_at DESC"""
    return db.session.execute(sql, {"addition_id": addition_id}).fetchall()

def add_review(addition_id, stars, comment, user_id,):
    sql = """INSERT INTO reviews (addition_id, stars, comment, user_id, visible, sent_at)
    VALUES (:addition_id, :stars, :comment, :user_id, 1, NOW())"""
    db.session.execute(sql, {"addition_id":addition_id, "stars":stars, "comment":comment, "user_id":user_id})
    db.session.commit()

def get_list():
    sql = """SELECT DISTINCT u.username, r.stars, r.comment FROM reviews r, users u,
    additions a WHERE r.user_id=u.id"""
    return db.session.execute(sql).fetchall()

def remove_review(addition_id):
    sql = "UPDATE reviews SET visible=0 WHERE id=:addition_id"
    db.session.execute(sql, {"addition_id":addition_id})
    db.session.commit()
