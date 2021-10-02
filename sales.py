from db import db
import users

def get_sales():
    sql = """SELECT S.comment, S.borough, U.username, S.sent_at, S.id FROM
    sales S, users U WHERE S.user_id=U.id AND S.visible=1 ORDER BY S.sent_at DESC"""
    result = db.session.execute(sql)
    return result.fetchall()
    
def send_sales_ad(comment, borough):
    creator_id = users.user_id()
    if creator_id == 0:
        return False
    sql = """INSERT INTO sales (comment, borough, user_id, sent_at, visible)
    VALUES (:comment, :borough, :creator_id, NOW(), 1)"""
    db.session.execute(sql, {"comment":comment, "borough":borough, "creator_id":creator_id})
    db.session.commit()
    return True

def get_my_sales(user_id):
    sql = """SELECT id, comment, borough FROM sales WHERE
    user_id=:user_id AND visible=1 ORDER BY id"""
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def remove_sale(sale_id, user_id):
    sql = "UPDATE sales SET visible=0 WHERE id=:id AND user_id=:user_id"
    db.session.execute(sql, {"id":sale_id, "user_id":user_id})
    db.session.commit()

def remove_sale_admin(addition_id):
    sql = "UPDATE sales SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":sale_id})
    db.session.commit()
