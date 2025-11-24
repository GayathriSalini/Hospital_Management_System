from flask_wtf import FlaskForm 
from wtforms import StringField,SelectField, PasswordField,BooleanField,TelField, TextAreaField, DateField, SubmitField, EmailField 
from wtforms.validators import DataRequired, Email, Length , Optional

class PatientRegisterForm(FlaskForm):
    p_name = StringField("Full Name", validators=[DataRequired(message="Name is required"), Length(max=225)])
    p_email = EmailField('Email', validators=[DataRequired(message="Email is required."),
        Email(message="enter a valid email address."), Length(max=225)])
    p_password = PasswordField('Password', validators=[DataRequired(message="Password is required"),Length(max=300)])
    p_address = TextAreaField('Address', validators=[DataRequired(message="Address is required"),Length(max=300)])
    p_dob = DateField('Date of the Birth', validators=[DataRequired(message="DOB is required")])
    p_tel = TelField('Phone Number (Optional)', validators=[Optional(),Length(max=10)])
    submit = SubmitField("REGISTER")
    

class PatientLoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Enter valid email address.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required.")
    ])
    submit = SubmitField("Login as Patient")

class DoctorLoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Enter valid email address.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required.")
    ])
    submit = SubmitField("Login as Doctor")

class AdminLoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Enter valid email address.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required.")
    ])
    submit = SubmitField("Login as Admin")
    
class AddPateintForm(FlaskForm):
    p_name = StringField("Full Name", validators=[DataRequired(message="Name is required"), Length(max=225)])
    p_email = EmailField('Email', validators=[DataRequired(message="Email is required."),
        Email(message="Enter valid email address."), Length(max=225)])
    p_password = PasswordField('Password', validators=[DataRequired(message="Password is required"),Length(max=300)])
    p_address = TextAreaField('Address', validators=[DataRequired(message="Address is required"),Length(max=300)])
    p_dob = DateField('Date of the Birth', validators=[DataRequired(message="DOB is required")])
    p_tel = TelField('Phone Number (Optional)', validators=[Optional(),Length(max=10)])
    submit = SubmitField("ADD PATIENT")
    
    
class AddDoctorForm(FlaskForm):
    doc_name = StringField("Full Name", validators=[DataRequired(message="Name is required"), Length(max=225)])
    doc_email = EmailField('Email', validators=[DataRequired(message="Email is required."),Length(max=225)])
    doc_password = PasswordField('Password', validators=[DataRequired(message="Password is required"),Length(max=300)])
    doc_nic = StringField("NIC", validators=[DataRequired(message="NIC is required"), Length(max=12)])
    doc_tel = TelField('Phone Number', validators=[DataRequired(message="Phone number is required"),Length(max=10)])
    specialty_id = SelectField("Specialty", coerce=int, validators=[DataRequired(message="Specialty is required")])
    submit = SubmitField("ADD DOCTOR")