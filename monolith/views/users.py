from flask import Blueprint, redirect, render_template, request
from monolith.database import db, User
from monolith.auth import admin_required, current_user
from monolith.forms import UserForm

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
            q = db.session.query(User).filter(User.email == form.email.data)
            user = q.first()
            if user is None:
                new_user = User()
                form.populate_obj(new_user)
                new_user.set_password(form.password.data)
                db.session.add(new_user)
                db.session.commit()
                return redirect('/')
            else: form.email.errors=["Seems like this email is already used"]
    return render_template('create_user.html', form=form)
