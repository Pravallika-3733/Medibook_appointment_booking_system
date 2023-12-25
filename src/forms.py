from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, SubmitField,SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired,ValidationError
from src.models import NewPatient, Patient, Doctor, NewDoctor
from src import db
from src import app

with app.app_context():
    db.create_all()
# --------------------------------------------------------- Appointment Form ------------------------------------------------------------------------
class AppointmentRequestForm(FlaskForm):
    doctor = SelectField('Choose Doctor', coerce=int, validators=[DataRequired()])
    appointment_date = DateField('Appointment Date', validators=[DataRequired()])
    submit = SubmitField('Submit Appointment Request')

    def __init__(self, *args, **kwargs):
        super(AppointmentRequestForm, self).__init__(*args, **kwargs)
        self.doctor.choices = [(0, 'Select Doctor')] + [(doctor.id, doctor.first_name) for doctor in Doctor.query.all()]

class AppointmentResponseForm(FlaskForm):
    action = SelectField('Action', choices=[('accept', 'Accept'), ('delete', 'Delete')], validators=[DataRequired()])
    submit = SubmitField('Submit')
# --------------------------------------------------------- Admin Login form ----------------------------------------------------------------------------
class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# --------------------------------------------------------- Admin Password reset form ----------------------------------------------------------------
class AdminPasswordResetForm(FlaskForm):
    new_email = StringField('New Email', validators=[DataRequired(),Email()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Update')

# ------------------------------------------------------ Patient Registration form --------------------------------------------------------------------
class RegisterForm(FlaskForm):
    def validate_email(self, email_to_check):
        email = NewPatient.query.filter_by(email=email_to_check.data).first() or Patient.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists! Please try a different email address')
        

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    date_of_birth = DateField(
        "Date of Birth",validators=[DataRequired()]
    )
    phone_number = StringField("Phone No", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters"),
            # Custom validator to ensure password contains letters and numbers
            lambda form, field: any(c.isalpha() for c in field.data)
            and any(c.isdigit() for c in field.data)
            or ("Password must contain letters and numbers"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    address = StringField("Address",validators=[DataRequired()])
    submit = SubmitField(label='Register')


# --------------------------------------------------------- Patient Login form -------------------------------------------------------------------------------
class PatientLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# ------------------------------------------------------ Patient details update form -----------------------------------------------------------------
class UpdatePatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update')

    
# ------------------------------------------------------ Doctor Registration form --------------------------------------------------------------------
class DoctorRegisterForm(FlaskForm):
    def validate_email(self, email_to_check):
        email = NewDoctor.query.filter_by(email=email_to_check.data).first() or Doctor.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists! Please try a different email address')
        

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    date_of_birth = DateField(
        "Date of Birth",validators=[DataRequired()]
    )
    phone_number = StringField("Phone No", validators=[DataRequired()])
    doctor_id = StringField("Doctor ID", validators=[DataRequired()])
    speciality = StringField("Speciality", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters"),
            # Custom validator to ensure password contains letters and numbers
            lambda form, field: any(c.isalpha() for c in field.data)
            and any(c.isdigit() for c in field.data)
            or ("Password must contain letters and numbers"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    address = StringField("Address",validators=[DataRequired()])
    submit = SubmitField(label='Register')

# --------------------------------------------------------- Doctor Login form ----------------------------------------------------------------------------
class DoctorLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# ------------------------------------------------------ Doctor details update form -----------------------------------------------------------------
class UpdateDoctorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    speciality = StringField("Speciality", validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update')
