from flask import request, flash, session, redirect, url_for, render_template
from datetime import datetime, timedelta, time
from . import doctor_bp
from models import DocSchedule, db, Doctor
from flask_login import login_required, current_user
from app.extensions import csrf


@csrf.exempt
@doctor_bp.route('/availability', methods=['GET', 'POST'])
@login_required
def availability():
    doctor_id = current_user.doc_id

    today = datetime.today().date()
    week_days = []
    for i in range(7):
        day = today + timedelta(days=i)
        fixed_time = time(hour=9, minute=0)
        week_days.append({'date': day, 'fixed_time': fixed_time})

   
    schedules = DocSchedule.query.filter(
        DocSchedule.doc_id == doctor_id,
        DocSchedule.schedule_date.between(today, today + timedelta(days=6))
    ).all()
    doctor = Doctor.query.get(doctor_id)

    if request.method == 'POST':
        mark_leave = request.form.get('mark_leave')  
        date_str = request.form.get('schedule_date')
        if not date_str:
            flash("Date not provided. Please try again.", "error")
            return redirect(url_for('doctor.availability'))

        try:
            schedule_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except Exception:
            flash("Invalid date format", "error")
            return redirect(url_for('doctor.availability'))

        if mark_leave == '1':

            schedule = DocSchedule.query.filter_by(doc_id=doctor_id, schedule_date=schedule_date).first()
            if schedule:
                schedule.title = "On Leave"
                schedule.nop = 0
                schedule.schedule_time = time(0, 0) 
            else:
                
                new_leave = DocSchedule(
                    doc_id=doctor_id,
                    title="On Leave",
                    schedule_date=schedule_date,
                    schedule_time=time(0, 0),
                    nop=0
                )
                db.session.add(new_leave)
            db.session.commit()
            
            return redirect(url_for('doctor.availability'))


        schedule_id = request.form.get('schedule_id')
        title = request.form.get('title')
        time_str = request.form.get('schedule_time')
        nop = request.form.get('nop')

        schedule_time = None
        shift_end_time = None
        if time_str:
            try:
                schedule_time = datetime.strptime(time_str, '%H:%M').time()
               
                dt = datetime.combine(schedule_date, schedule_time)
                dt_end = dt + timedelta(hours=8)
                shift_end_time = dt_end.time()
            
            
            except Exception:
                return redirect(url_for('doctor.availability'))

        try:
            nop_val = int(nop) if nop else 20
            if nop_val is not None and nop_val < 0:
                raise ValueError()
        except ValueError:
            flash("Number of slots give again", "danger")
            return redirect(url_for('doctor.availability'))

        if schedule_id:
            schedule = DocSchedule.query.get(schedule_id)
            if schedule and schedule.doc_id == doctor_id:
                schedule.title = title
                schedule.schedule_date = schedule_date
                schedule.schedule_time = schedule_time
                schedule.nop = nop_val
                db.session.commit()
                flash("Schedule updated successfully", "success")
            else:
                flash("Schedule not found or unauthorized", "error")
        else:
            new_schedule = DocSchedule(
                doc_id=doctor_id,
                title=title,
                schedule_date=schedule_date,
                schedule_time=schedule_time,
                nop=nop_val
            )
            db.session.add(new_schedule)
            db.session.commit()
            flash("Availability added", "success")


        return redirect(url_for('doctor.availability'))

    return render_template(
        'doctor/availability.html', week_days=week_days, schedules=schedules, doctor=doctor
    )