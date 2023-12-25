from flask import render_template, url_for, redirect, flash, session, request
from src.models import NewPatient, Patient, NewDoctor, Doctor, Admin, Appointment
from src.forms import RegisterForm, PatientLoginForm, DoctorRegisterForm, DoctorLoginForm, AdminLoginForm, AdminPasswordResetForm, AppointmentRequestForm, UpdatePatientForm, UpdateDoctorForm, AppointmentResponseForm
from src import app, db

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def registration():
    return render_template('registration.html')
# -------------------------------------------------------------------- Admin Routes ------------------------------------------------------------------
@app.route('/admin/dashboard')
def admin_dashboard():
    form = AdminPasswordResetForm()
    admin_id=session.get('admin_id')
    if admin_id:
        patients = Patient.query.all()
        newpatients = NewPatient.query.all()
        doctors = Doctor.query.all()
        newdoctors = NewDoctor.query.all()
        return render_template('/admin/admin_dashboard.html', patients=patients,newpatients=newpatients,doctors=doctors,newdoctors=newdoctors,form=form)
    else:
        flash('Please log in first.',category='danger')
        return redirect('/admin/login')
    

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if  session.get('admin_id'):
        return redirect('/admin/dashboard')
    else: 
        form = AdminLoginForm()
        
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            
            admin = Admin.query.filter_by(email=email, password=password).first()
            if admin:
                flash('Login successful!',category='success')
                # Redirect to admin dashboard or other admin functionality
                session['admin_id'] = admin.id
                return redirect('/admin/dashboard')
            else:
                flash('Invalid credentials. Please try again.',category='danger')
        
        return render_template('/admin/admin_login.html', form=form)



@app.route('/admin/update', methods=['GET', 'POST'])
def admin_update():
    form = AdminPasswordResetForm()
    admin_id=session.get('admin_id')

    admin = Admin.query.get(admin_id)
    if not admin:
        flash('Admin not found.',category='danger')
        return redirect('/admin/login')

    if form.validate_on_submit():
        new_email = form.new_email.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data
        
        if new_password == confirm_password:
            if new_email:
                admin.email = new_email
            admin.password = new_password
            db.session.commit()
            flash('Admin Details Updated successfully..',category='success')
            return redirect('/admin/login')
        else:
            flash('Passwords do not match.',category='danger')

    return render_template('/admin/admin_update.html', form=form)



@app.route('/admin/approve_patient/<int:new_patient_id>', methods=['POST'])
def approve_patient(new_patient_id):
    new_patient = NewPatient.query.get(new_patient_id)
    if new_patient:
        patient_data = {
            'first_name': new_patient.first_name,
            'last_name': new_patient.last_name,
            'email': new_patient.email,
            'date_of_birth': new_patient.date_of_birth,
            'phone_number': new_patient.phone_number,
            'password_hash': new_patient.password_hash,
            'address': new_patient.address,
        }
        
        # Create a new entry in the Patient model
        patient = Patient(**patient_data)
        db.session.add(patient)
        db.session.commit()
        
        # Delete the entry from NewPatient
        db.session.delete(new_patient)
        db.session.commit()
        
        flash('Patient approved successfully.',category='success')

    return redirect('/admin/dashboard')


@app.route('/admin/delete_patient/<int:new_patient_id>', methods=['POST'])
def delete_patient(new_patient_id):
    patient = NewPatient.query.get(new_patient_id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
        flash('Patient deleted successfully.')
        # Notify patient about deletion if needed
    return redirect('/admin/dashboard')

@app.route('/admin/delete/patient/<int:patient_id>', methods=['POST'])
def delete_existing_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
        flash('Patient deleted successfully.')
        # Notify patient about deletion if needed
    return redirect('/admin/dashboard')


@app.route('/admin/approve_doctor/<int:new_doctor_id>', methods=['POST'])
def approve_doctor(new_doctor_id):
    new_doctor = NewDoctor.query.get(new_doctor_id)
    if new_doctor:
        doctor_data = {
            'first_name': new_doctor.first_name,
            'last_name': new_doctor.last_name,
            'doctor_id': new_doctor.doctor_id,
            'speciality': new_doctor.speciality,
            'email': new_doctor.email,
            'date_of_birth': new_doctor.date_of_birth,
            'phone_number': new_doctor.phone_number,
            'password_hash': new_doctor.password_hash,
            'address': new_doctor.address,
            # Add other fields here...
        }
        
        # Create a new entry in the Patient model
        doctor = Doctor(**doctor_data)
        db.session.add(doctor)
        db.session.commit()
        
        # Delete the entry from NewPatient
        db.session.delete(new_doctor)
        db.session.commit()
        
        flash('Doctor approved successfully.')
    return redirect('/admin/dashboard')

@app.route('/admin/delete_doctor/<int:new_doctor_id>', methods=['POST'])
def delete_doctor(new_doctor_id):
    doctor = NewDoctor.query.get(new_doctor_id)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        flash('Doctor deleted successfully.')

    return redirect('/admin/dashboard')

@app.route('/admin/delete/doctor/<int:doctor_id>', methods=['POST'])
def delete_existing_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        flash('Doctor deleted successfully.')

    return redirect('/admin/dashboard')

@app.route('/admin/logout', methods=['GET', 'POST'])
def admin_logout():
    if not session.get('admin_id'):
        return redirect('/admin/login')
    if session.get('admin_id'):
        session.pop('admin_id', None)
        return redirect('/admin/login')
# -------------------------------------------------------------------- Doctor Routes -----------------------------------------------------------------
@app.route('/doctor/dashboard', methods=['GET', 'POST'])
def doctor_dashboard():
    form = AppointmentResponseForm()
    patients = Patient.query.all()
    doctor_id = session.get('doctor_id')
    if doctor_id:
        # Fetch patient's specific data from the database using patient_id
        doctor = Doctor.query.get(doctor_id)
        appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()

        if doctor:
            if form.validate_on_submit():
                action = form.action.data
                appointment_id = request.form['appointment_id']
                appointment = Appointment.query.get(appointment_id)
                
                if appointment:
                    if action == 'accept':
                        appointment.status = 'accepted'
                        flash('Appointment accepted!',category='success')
                    elif action == 'delete':
                        appointment.status = 'deleted'
                        flash('Appointment deleted!',category='danger')
                    db.session.commit()
                    return redirect(url_for('doctor_dashboard'))

            
            return render_template('/doctor/doctor_dashboard.html', doctor=doctor,patients=patients,appointments=appointments,form=form)
        else:
            flash('Doctor data not found.',category='danger')
            return redirect('/doctor/login')
    else:
        flash('Please log in first.',category='danger')
        return redirect('/doctor/login')


@app.route('/doctor/register', methods=['GET', 'POST'])
def doctor_register():
    form = DoctorRegisterForm()
    if form.validate_on_submit():
        new_doctor = NewDoctor(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            doctor_id=form.doctor_id.data,
            speciality=form.speciality.data,
            email=form.email.data,
            date_of_birth=form.date_of_birth.data,
            phone_number=form.phone_number.data,
            password=form.password.data,
            address=form.address.data,
        )
        db.session.add(new_doctor)
        db.session.commit()

        flash('Your registration request has been sent to the Super Admin for approval.', category='success')
        return redirect(url_for('doctor_register'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('/doctor/doctor_registration.html', form=form)


@app.route('/doctor/login', methods=['GET', 'POST'])
def doctor_login():
    if  session.get('doctor_id'):
        return redirect('/doctor/dashboard')
    else:    
        form = DoctorLoginForm()

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            # Check if the provided credentials exist in the Patient model
            doctor = Doctor.query.filter_by(email=email).first()
            newdoctor = NewDoctor.query.filter_by(email=email).first()
            if newdoctor:
                flash('Your registration is still pending approval.', category='warning')
            elif doctor and doctor.check_password_correction(
                    attempted_password=password
            ):
                flash(f'Success! You are logged in as: {doctor.first_name}', category='success')
                session['doctor_id'] = doctor.id
                return redirect('/doctor/dashboard')
            else:
                flash('Invalid credentials. Please try again.',category='danger')

        return render_template('/doctor/doctor_login.html', form=form)

@app.route('/doctor/update_profile', methods=['GET', 'POST'])
def doctor_update_profile():
    patient_id = session.get('doctor_id') 
    
    doctor = Doctor.query.get(patient_id)
    form = UpdateDoctorForm(obj=doctor)

    if form.validate_on_submit():
        form.populate_obj(doctor)
        db.session.commit()
        flash(f'Doctor details updated successfully....', category='success')
        return redirect(url_for('doctor_dashboard'))

    return render_template('doctor/doctor_update_profile.html', form=form)

@app.route('/doctor/logout', methods=['GET', 'POST'])
def doctor_logout():
    if not session.get('doctor_id'):
        return redirect('/doctor/login')
    if session.get('doctor_id'):
        session.pop('doctor_id', None)
        return redirect('/doctor/login')
# -------------------------------------------------------------------- Patient Routes ----------------------------------------------------------------
@app.route('/patient/dashboard', methods=['GET', 'POST'])
def patient_dashboard():
    form = AppointmentRequestForm()
    Appointments=Appointment.query.all()
    patient_id = session.get('patient_id')
    if patient_id:
        patient = Patient.query.get(patient_id)

        if patient:
                if form.validate_on_submit():   
                    doctor_id = form.doctor.data
                    appointment_date = form.appointment_date.data
                    new_appointment = Appointment(
                        patient_id=patient.id,
                        doctor_id=doctor_id,
                        appointment_date=appointment_date
                    )
                    db.session.add(new_appointment)
                    db.session.commit()
                    flash('Appointment request sent!',category='success')
                    return render_template('/patient/patient_dashboard.html', patient=patient,Appointments=Appointments , form=form)    
                
                accepted_appointments = Appointment.query.join(Doctor, Appointment.doctor_id == Doctor.id).\
                    filter(Appointment.patient_id == patient.id).\
                    add_columns(Doctor.first_name, Appointment.appointment_date, Appointment.status).all()
                
                return render_template('/patient/patient_dashboard.html', patient=patient,form=form,Appointments=Appointments,accepted_appointments=accepted_appointments)
        else:
            flash('Patient data not found.',category='danger')
            return redirect('/patient/login')
    else:
        flash('Please log in first.',category='danger')
        return redirect('/patient/login')
    

@app.route('/patient/register', methods=['GET', 'POST'])
def patient_register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_patient = NewPatient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            date_of_birth=form.date_of_birth.data,
            phone_number=form.phone_number.data,
            password=form.password.data,
            address=form.address.data,
        )
        db.session.add(new_patient)
        db.session.commit()

        flash('Your registration request has been sent to the Super Admin for approval.', category='success')
        return redirect(url_for('patient_register'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('/patient/patient_registration.html', form=form)


@app.route('/patient/login', methods=['GET', 'POST'])
def patient_login():
    if  session.get('patient_id'):
        return redirect('/patient/dashboard')
    else:
        form = PatientLoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            # Check if the provided credentials exist in the Patient model
            patient = Patient.query.filter_by(email=email).first()
            newpatient = NewPatient.query.filter_by(email=email).first()
            if newpatient:
                flash('Your registration is still pending approval.', category='warning')
            elif patient and patient.check_password_correction(attempted_password=password):
                    session['patient_id'] = patient.id
                    flash(f'Success! You are logged in as: {patient.first_name}', category='success')
                    return redirect(url_for('patient_dashboard'))
            else:
                flash('Invalid credentials. Please try again.', category='danger')

        return render_template('/patient/patient_login.html', form=form)

@app.route('/patient/update_profile', methods=['GET', 'POST'])
def patient_update_profile():
    patient_id = session.get('patient_id') 
    
    patient = Patient.query.get(patient_id)
    form = UpdatePatientForm(obj=patient)

    if form.validate_on_submit():
        form.populate_obj(patient)
        db.session.commit()
        flash(f'Patient details updated successfully....', category='success')
        return redirect(url_for('patient_dashboard'))

    return render_template('patient/patient_update_profile.html', form=form)

@app.route('/patient/logout', methods=['GET', 'POST'])
def patient_logout():
    if not session.get('patient_id'):
        return redirect('/patient/login')

    if session.get('patient_id'):
        session.pop('patient_id', None)
        return redirect('/patient/login')