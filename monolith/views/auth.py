from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from sqlalchemy.exc import IntegrityError
from monolith.database import db, User
from monolith.forms import LoginForm, UserForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_anonymous:
        return redirect("/", code=302)
    form = LoginForm()
    if len(request.args)>0 :
        message= request.args.get('message', None)
        #this parameter can be passed through the url to display different types of messages
        #see create_user method
        form.message= message 
    if form.validate_on_submit():
        email, password = form.data['email'], form.data['password']
        q = db.session.query(User).filter(User.email == email)
        user = q.first()
        if user is not None and user.authenticate(password):
            login_user(user)
            return redirect('/')
        else:
            return redirect(url_for('auth.login', message="User or Password not correct!"))
    return render_template('login.html', form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@auth.route('/signup', methods=['GET', 'POST'])
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
