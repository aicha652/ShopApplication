# Define the forms used by the application
from flask_wtf import FlaskForm
from wtforms import StringField, StringField, PasswordField, validators, ValidationError, SubmitField, IntegerField, TextAreaField
from wtforms.validators import Email, DataRequired, EqualTo
from flask_wtf.file import FileAllowed, FileField
from .models import User
from .tools import verify_pass


class UserForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe',
                             id='pwd_create',
                             validators=[DataRequired(),
                                         EqualTo('confirm',
                                                 message='Le mot de passe de confirmation est incorrect')])
    confirm = PasswordField("Repeat Password", [validators.DataRequired()])    
    country = StringField('Country', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])
    phone = StringField('Phone', [validators.DataRequired()])
    
    submit = SubmitField("Register")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already Exists.")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already Exists.")

class EditUserForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    country = StringField('Country', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])
    phone = StringField('Phone', [validators.DataRequired()])


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])  
    submit = SubmitField('Login')


class AddProducts(FlaskForm):
    name = StringField("Name", [validators.DataRequired()])
    price = IntegerField("Price ", [validators.DataRequired()])
    desc = TextAreaField("Description", [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[validators.DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'svg', 'gif'])])
