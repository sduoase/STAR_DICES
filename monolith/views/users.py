from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from monolith.database import db, User, Story, Follow
from monolith.auth import admin_required, current_user
from sqlalchemy.exc import IntegrityError

users = Blueprint('users', __name__)

@users.route('/users')
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)

@users.route('/my_wall')
@login_required
def index():
    stories = db.session.query(Story).filter(Story.author_id == current_user.id)
    return render_template("mywall.html", stories=stories)

@users.route('/wall/<author_id>/follow', methods=['GET'])
@login_required
def follow(author_id):
    db.session.add(Follow(author_id, current_user.id))
    message = ''
    try:
        db.session.commit()
        message = "Following!"
    except IntegrityError:
        message = "Already following!"
    
    return render_template('follow.html', message = message)

@users.route('/wall/<author_id>/unfollow', methods=['GET'])
@login_required
def unfollow(author_id):
    Follow.query.filter(Follow.user_id == author_id, Follow.followed_by_id == current_user.id).delete()
    db.session.commit()

    return render_template('follow.html', message = "Unfollowed!")
