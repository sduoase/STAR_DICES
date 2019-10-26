from flask import Blueprint, redirect, render_template, request, url_for
from monolith.database import db, User
from monolith.auth import admin_required, current_user
from monolith.forms import UserForm, LoginForm
from sqlalchemy.exc import IntegrityError

users = Blueprint('users', __name__)

@users.route('/users')
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)


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
