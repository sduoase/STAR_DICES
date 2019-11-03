from flask import Blueprint, redirect, render_template, request, url_for, abort
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from monolith.database import db, User, Story, Follow, isFollowing
from monolith.auth import admin_required, current_user
from sqlalchemy.exc import IntegrityError

users = Blueprint('users', __name__)

@users.route('/users')
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)

@users.route('/my_wall')
@login_required
def my_wall():
    stories = db.session.query(Story).filter(Story.author_id == current_user.id)
    return render_template("mywall.html", stories=stories)

@users.route('/wall/<author_id>', methods=['GET'])
@login_required
def wall(author_id):
    author = User.query.filter_by(id = author_id).first()
    if author is None:
        abort(404)

    stories = Story.query.filter_by(author_id = author_id)
    return render_template("wall.html", stories=stories, author=author, alreadyFollowing = isFollowing(author_id, current_user.id))

@users.route('/wall/<author_id>/follow', methods=['GET'])
@login_required
def follow(author_id):
    author = User.query.filter_by(id = author_id).first()
    if author is None:
        abort(404)

    db.session.add(Follow(author_id, current_user.id))
    try:
        db.session.commit()
        message = "Following!"
    except IntegrityError:
        message = "Already following!"

    return render_template('message.html', message=message)

@users.route('/wall/<author_id>/unfollow', methods=['GET'])
@login_required
def unfollow(author_id):
    author = User.query.filter_by(id = author_id).first()
    if author is None:
        abort(404)

    if isFollowing(author_id, current_user.id):
        Follow.query.filter(Follow.user_id == author_id, Follow.followed_by_id == current_user.id).delete()
        db.session.commit()
        message = "Unfollowed!"
    else:
        message = "You were not following that particularly user!"
    return render_template('message.html', message=message)

@users.route('/my_wall/followers', methods=['GET'])
@login_required
def my_followers():
    return render_template('myfollowers.html',
                           followers = db.session.query(User).join(Follow, User.id == Follow.followed_by_id)
                                                             .filter(Follow.user_id == current_user.id)
                                                             .filter(Follow.followed_by_id != current_user.id)
                                                             .all())
