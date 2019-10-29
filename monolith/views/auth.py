from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import (current_user, login_user, logout_user,
                         login_required)

from monolith.database import db, User
from monolith.forms import LoginForm

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
