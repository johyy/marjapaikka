import os
from db import db
from flask import abort, request, session
import users

def get_list():
	sql = "SELECT A.borough, A.genre, A.coordinates, U.username, A.sent_at FROM additions A, users U WHERE A.user_id=U.id ORDER BY A.sent_at" 
	result = db.session.execute(sql)
	return result.fetchall()

def send(borough, genre, coordinates):
	user_id = users.user_id()
	if user_id == 0:
		return False
	sql = "INSERT INTO additions (borough, genre, coordinates, user_id, sent_at) VALUES (:borough, :genre, :coordinates, :user_id, NOW())"
	db.session.execute(sql, {"borough":borough, "genre":genre, "coordinates":coordinates, "user_id":user_id})
	db.session.commit()
	return True
