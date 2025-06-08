from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from utils.data_manager import DataManager

app = Flask(__name__)
app.secret_key = 'healthtrack-secret-key'  # Flash mesajları için gerekli
Bootstrap(app)

data_manager = DataManager()

@app.route('/')
def index():
    """Ana sayfa"""
    today_schedule = data_manager.get_today_schedule()
    users = data_manager.get_all_users()
    return render_template('index.html', 
                         schedule=today_schedule,
                         users=users,
                         today=datetime.now().strftime("%Y-%m-%d"))

@app.route('/users', methods=['GET', 'POST'])
def users():
    """Kullanıcı yönetimi sayfası"""
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        health_status = request.form.get('health_status')
        
        if name and age and health_status:
            data_manager.add_user(name, int(age), health_status)
            flash('Kullanıcı başarıyla eklendi!', 'success')
            return redirect(url_for('users'))
    
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    """Randevu yönetimi sayfası"""
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        date = request.form.get('date')
        time = request.form.get('time')
        description = request.form.get('description')
        
        if all([user_id, date, time, description]):
            data_manager.add_appointment(int(user_id), date, time, description)
            flash('Randevu başarıyla eklendi!', 'success')
            return redirect(url_for('appointments'))
    
    users = data_manager.get_all_users()
    today_schedule = data_manager.get_today_schedule()
    return render_template('appointments.html', 
                         users=users,
                         appointments=today_schedule['appointments'])

@app.route('/medications', methods=['GET', 'POST'])
def medications():
    """İlaç takibi sayfası"""
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        time = request.form.get('time')
        frequency = request.form.get('frequency')
        
        if all([user_id, name, time, frequency]):
            data_manager.add_medication(int(user_id), name, time, frequency)
            flash('İlaç başarıyla eklendi!', 'success')
            return redirect(url_for('medications'))
    
    users = data_manager.get_all_users()
    today_schedule = data_manager.get_today_schedule()
    return render_template('medications.html', 
                         users=users,
                         medications=today_schedule['medications'])

if __name__ == '__main__':
    app.run(debug=True) 