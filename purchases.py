from db import db
import users

def get_purchases():
    sql = """SELECT P.comment, P.borough, U.username, P.sent_at, P.id FROM
    purchases P, users U WHERE P.user_id=U.id AND P.visible=1 ORDER BY P.sent_at DESC"""
    result = db.session.execute(sql)
    return result.fetchall()

def send_ad(comment, borough):
    creator_id = users.user_id()
    if creator_id == 0:
        return False
    sql = """INSERT INTO purchases (comment, borough, user_id, sent_at, visible)
    VALUES (:comment, :borough, :creator_id, NOW(), 1)"""
    db.session.execute(sql, {"comment":comment, "borough":borough, "creator_id":creator_id})
    db.session.commit()
    return True

def get_my_purchases(user_id):
    sql = """SELECT id, comment, borough FROM purchases WHERE
    user_id=:user_id AND visible=1 ORDER BY id"""
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def remove_purchase(purchase_id, user_id):
    sql = "UPDATE purchases SET visible=0 WHERE id=:id AND user_id=:user_id"
    db.session.execute(sql, {"id":purchase_id, "user_id":user_id})
    db.session.commit()

def remove_purchase_admin(purchase_id):
    sql = "UPDATE purchases SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":purchase_id})
    db.session.commit()
