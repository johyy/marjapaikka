import os
from db import db
from flask import abort, request, session
import users, additions


def get_reviews(addition_id):
    sql = """SELECT u.name, r.stars, r.comment FROM reviews r, users u, additions a
             WHERE r.user_id=u.id AND r.addition_id=:a.id ORDER BY r.id"""
    return db.session.execute(sql, {"addition_id": addition_id}).fetchall()
    
def add_review(addition_id, user_id, stars, comment):
    sql = """INSERT INTO reviews (addition_id, stars, comment, user_id,)
             VALUES (:addition_id, :stars, :comment, :user_id)"""
    db.session.execute(sql, {"addition_id":addition_id, "stars":stars, "comment":comment, "user_id":user_id})
    db.session.commit()
