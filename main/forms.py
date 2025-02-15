from secrets import choice
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from flask_login import current_user
from wtforms import MultipleFileField
from wtforms import StringField,PasswordField,TextAreaField, SelectField,SubmitField, BooleanField, TextField,FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from main.models import User
class RegistrationForm(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired(),Length(min=2,max=50)])
    lastname = StringField('lastname', validators=[DataRequired(),Length(min=2,max=50)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    picture = FileField('Image', validators=[ DataRequired(),FileAllowed(['jpg','png','jpeg'])])
    password = PasswordField('Password',validators=[DataRequired(),Regexp('[A-Za-z0-9@#$%^&+=]{8,}',message='Password not valid, example : Password123!')])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Create a new account')
    def validate_email(self,email):
        email_user = User.query.filter_by(email= email.data).first()
        if email_user:
            raise ValidationError('That email is taken, please use a different one!')

class editUser(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired(),Length(min=2,max=50)])
    lastname = StringField('lastname', validators=[DataRequired(),Length(min=2,max=50)])
    picture = FileField('Image', validators=[ FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Sign Up')
    
    # def validate_email(self,email):
    #     email_user = User.query.filter_by(email= email.data).first()
    #     if email_user and not email_user.id == self.id:
    #         raise ValidationError('That email is taken, please use a different one!')
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')


class addPost(FlaskForm):
    title = StringField('Post title',validators=[DataRequired()])
    text = TextAreaField(render_kw={"rows":3, "cols": 4}) 
    picture = FileField('Image', validators=[ FileAllowed(['jpg','png','jpeg'])])
    category = SelectField('Category',validators=[DataRequired()], choices=["Business","People","Food","Events"])
    column = SelectField('Column',validators=[DataRequired()], choices=[1,2,3])
    alt_text = StringField('Description',validators=[DataRequired()])
    submit = SubmitField('Submit')
    back = SubmitField('Back')


class editPost(FlaskForm):
    title = StringField('Post title',validators=[DataRequired()])
    text = TextAreaField(render_kw={"rows":5, "cols": 4}) 
    picture = FileField('Image', validators=[ FileAllowed(['jpg','png','jpeg'])])
    category = SelectField('Category',validators=[DataRequired()], choices=["Business","People","Food","Events"])
    column = SelectField('Column',validators=[DataRequired()], choices=[1,2,3])
    alt_text = StringField('Description',validators=[DataRequired()])
    submit = SubmitField('Submit')
    back = SubmitField('Back')

class editCategory(FlaskForm):
    title = StringField('Category',validators=[DataRequired()])
    description = TextAreaField(render_kw={"rows":5, "cols": 4},validators=[DataRequired()]) 
    picture = FileField('Image',validators=[ FileAllowed(['jpg','png','jpeg'])])
    alt_text = StringField('Description',validators=[DataRequired()])
    submit = SubmitField('Submit')

class addCategory(FlaskForm):
    title = StringField('Category',validators=[DataRequired()])
    description = TextAreaField(render_kw={"rows":5, "cols": 4},validators=[DataRequired()]) 
    picture = FileField('picture',validators=[ FileAllowed(['jpg','png','jpeg'])])
    alt_text = StringField('Description',validators=[DataRequired()])
    submit = SubmitField('Submit')



class SendEmail(FlaskForm):
    customer_email = StringField('Email',validators=[Email(),DataRequired()])
    name = StringField('Name',validators=[DataRequired()])
    surname = StringField('Surname',validators=[DataRequired()])
    phoneno= StringField('Phone number',validators=[DataRequired()])
    text = TextAreaField('Type your message here!',render_kw={"rows":5, "cols": 11})
    submit = SubmitField('Contanct me')

class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')
        
    def validate_email(self,email):
        email_user = User.query.filter_by(email= email.data).first()
        if email_user is None:
            raise ValidationError('There is no account with that email. You must register first.')
class ResetPassword(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired(),Regexp('[A-Za-z0-9@#$%^&+=]{8,}',message='Password not valid, example : Password123!')])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')
class ConfirmEmail(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Confirm Email')
        
    def validate_email(self,email):
        email_user = User.query.filter_by(email= email.data).first()
        if email_user is None:
            raise ValidationError('There is no account with that email. You must register first.')
