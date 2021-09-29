from db import db
import users, reviews

def get_list():
    sql = """SELECT A.borough, A.genre, A.coordinates, U.username, A.sent_at, A.id FROM
    additions A, users U WHERE A.creator_id=U.id AND A.visible=1 ORDER BY A.sent_at DESC"""
    result = db.session.execute(sql)
    return result.fetchall()

def get_addition_info(addition_id):
    sql = """SELECT a.borough, a,genre, u.username FROM additions a, users u WHERE
    a.id=:addition_id AND a.creator_id=u.id;"""
    return db.session.execute(sql, {"addition_id": addition_id}).fetchone()

def send(borough, genre, coordinates):
    creator_id = users.user_id()
    if creator_id == 0:
        return False
    sql = """INSERT INTO additions (borough, genre, coordinates, creator_id, sent_at, visible)
    VALUES (:borough, :genre, :coordinates, :creator_id, NOW(), 1)"""
    db.session.execute(sql, {"borough":borough, "genre":genre, "coordinates":coordinates, "creator_id":creator_id})
    db.session.commit()
    return True
	
def get_my_additions(user_id):
    sql = """SELECT id, borough, genre, coordinates FROM additions WHERE
    creator_id=:user_id AND visible=1 ORDER BY id"""
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def remove_addition(addition_id, user_id):
    sql = "UPDATE additions SET visible=0 WHERE id=:id AND creator_id=:user_id"
    db.session.execute(sql, {"id":addition_id, "user_id":user_id})
    db.session.commit()

def add_review(addition_id, stars, comment, user_id,):
    sql = """INSERT INTO reviews (addition_id, stars, comment, user_id) VALUES
    (:addition_id, :stars, :comment, :user_id)"""
    db.session.execute(sql, {"addition_id":addition_id, "stars":stars, "comment":comment, "user_id":user_id})
    db.session.commit()

def get_reviews(addition_id):
    sql = """SELECT u.username, r.stars, r.comment FROM reviews r, users u
    WHERE r.user_id=u.id AND r.addition_id=:addition_id ORDER BY r.id"""
    return db.session.execute(sql, {"addition_id": addition_id}).fetchall()
