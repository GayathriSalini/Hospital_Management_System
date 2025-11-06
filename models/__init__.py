from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .admin import Admin
from .doctor import Doctor
from .appointment import Appointment
from .patient import Patient
from .patient_details import PatientDetails
from .treatment import Treatment
from .doc_schedule import DocSchedule
from .specialities import Specialities 
from .webuser import WebUser 