from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from monolith.database import db, User, Story, Follow
from monolith.auth import admin_required, current_user

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

@users.route('/signup', methods=['GET', 'POST'])
def create_user():
    if not current_user.is_anonymous:
        return redirect("/", code=302)
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user = User()
        form.populate_obj(new_user)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
            return redirect(url_for("auth.login", message="You have been sucessfully registered!"))
        except IntegrityError:
            db.session.rollback()
            form.message="Seems like this email is already used"
            
    return render_template('create_user.html', form=form)


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

    return render_template('follow.html', message = "Unfollowed!")
