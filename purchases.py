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
