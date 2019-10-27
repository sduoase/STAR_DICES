from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired, Email, Length

MAX_CHAR_STORY = 1000
MIN_CHAR_PWD = 10
MAX_CHAR_PWD = 20

class LoginForm(FlaskForm):
    email = f.StringField('email', validators=[DataRequired(), Email(message="Not a valid email.")])
    password = f.PasswordField('password', validators=[DataRequired()])
    display = ['email', 'password']


class UserForm(FlaskForm):
    email = f.StringField('email', validators=[DataRequired(), Email(message="Not a valid email.")])
    firstname = f.StringField('firstname', validators=[DataRequired()])
    lastname = f.StringField('lastname', validators=[DataRequired()])
    password = f.PasswordField('password', validators=[DataRequired(),
                                                       Length(MIN_CHAR_PWD,
                                                              MAX_CHAR_STORY,
                                                              message="At least "+str(MIN_CHAR_PWD)+" characters..")
                                                       ])
    dateofbirth = f.DateField('dateofbirth', format='%d/%m/%Y')
    display = ['email', 'firstname', 'lastname', 'password', 'dateofbirth']

class StoryForm(FlaskForm):
    text = f.TextField('text', validators=[DataRequired(),
                                           Length(-1,
                                                  MAX_CHAR_STORY,
                                                  message="Reach max number of characters!")
                                           ]) #TODO: Add check on length (1000 chrs)
    display = ['text']