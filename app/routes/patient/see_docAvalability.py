from  flask import request , session, redirect, url_for, flash, render_template
from models import Patient, Doctor, DocSchedule, db
from . import patient_bp
from datetime import datetime, timedelta, time

@patient_bp.route('/doctor_availability/<int:doc_id>')
def doc_availability(doc_id):
    doctor = Doctor.query.get_or_404(doc_id)
    
    
    today = datetime.today().date()
    days = [today + timedelta(days=i) for i in range(7)]
    
    
    
    schedules = DocSchedule.query.filter(
        DocSchedule.doc_id == doc_id,
        DocSchedule.schedule_date >= today,
        DocSchedule.schedule_date <= days[-1]  # last day in range
    ).all()
    
    schedule = {sched_doc.schedule_date: sched_doc for sched_doc in schedules}
    docshed_see = []
    for day in days :
        sched_doc = schedule.get(day)
        if sched_doc:
            if sched_doc.schedule_time != time(0,0) and sched_doc.nop!=0:
                 docshed_see.append(sched_doc) 
    
        else:
            docshed_see.append(DocSchedule(
                schedule_date=day,
                schedule_time=time(9,0),
                nop=20
            ))
                
                
                
    return render_template('patient/doc_availability.html', doctor=doctor, schedules=docshed_see)
