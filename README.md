# Hospital Management System

_A smart, streamlined web app that digitizes hospital management — managing patients, doctors, appointments, and treatments with ease and security._

## 🚀 Introduction
NHS Health Management System built with Flask and SQLite provides role-based dashboards for Admin, Doctors, and Patients with smart scheduling and data visualization.

## ✨ Features
- Role-based access control (Admin, Doctor, Patient)
- Admin dashboard to manage doctors, patients, schedules, and analytics
- Doctors can view appointments and record treatments
- Patients can book and reschedule appointments respecting doctor availability
- Interactive charts for data insights
- Secure authentication and form handling

## 💾 Complete Setup & Run Commands

### **Option 1: Quick Start (No Virtual Environment)**
Step 1: Clone/Download the project folder
git clone https://github.com/24f3000207/hospital-management-system.git

cd hospital-management-system

Step 2: Install required packages globally
pip install flask flask-sqlalchemy flask-login flask-wtf flask-migrate werkzeug

Step 3: Create database tables
python -c "from app import app, db; with app.app_context(): db.create_all()"

Step 4: Run the application
python app.py

text

### **Option 2: Recommended (With Virtual Environment)**
Step 1: Clone/Download the project folder
git clone https://github.com/24f3000207/hospital-management-system.git
cd hospital-management-system

Step 2: Create & activate virtual environment
python -m venv venv

Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate

Step 3: Install all dependencies
pip install -r requirements.txt

Step 4: Set Flask environment
export FLASK_APP=app.py
export FLASK_ENV=development

Windows (Command Prompt):
set FLASK_APP=app.py
set FLASK_ENV=development

Step 5: Create database tables
python -c "from app import app, db; with app.app_context(): db.create_all()"

Step 6: Run the application
flask run

OR simply:
python app.py

**✅ Open your browser: http://127.0.0.1:5000**

## 🔑 Default Admin Login
**Email:** [admin@nhshospital.com](mailto:admin@nhshospital.com) **|** **Password:** admin@NHShospital

