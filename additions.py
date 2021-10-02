from db import db
import users 
import reviews

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

def remove_addition_admin(addition_id):
    sql = "UPDATE additions SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":addition_id})
    db.session.commit()

def get_result(query):
    sql = """SELECT A.borough, A.genre, A.coordinates, U.username, A.sent_at, A.id FROM
    additions A, users U  WHERE A.creator_id=U.id AND A.visible=1 AND A.genre LIKE :query ORDER BY A.sent_at DESC"""
    return db.session.execute(sql, {"query":"%"+query+"%"}).fetchall()

