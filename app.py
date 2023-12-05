from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from datetime import datetime

app = Flask(__name__)

# Пример расписания в виде словаря (в реальном приложении данные следует хранить в базе данных).
schedule = {
    'Понедельник': [{'start_time': '09:00', 'end_time': '11:00', 'subject': 'Математика'}],
    'Вторник': [{'start_time': '10:00', 'end_time': '14:00', 'subject': 'Химия'}],
    'Среда': [{'start_time': '09:30', 'end_time': '13:30', 'subject': 'История'}],
    # ... остальные дни недели
}

# Пример списка пользователей с правами на изменение расписания.
authorized_users = {'admin': 'пароль123'}

def get_day_of_week(date_string):
    # Получаем день недели на русском языке по переданной дате.
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    date_obj = datetime.strptime(date_string, '%Y-%m-%d')
    return days[date_obj.weekday()]

@app.route('/')
def index():
    today = datetime.now().strftime('%Y-%m-%d')
    selected_date = request.args.get('date', today)
    selected_day = get_day_of_week(selected_date)
    return render_template('index.html', schedule=schedule, selected_date=selected_date, selected_day=selected_day)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in authorized_users and authorized_users[username] == password:
            return redirect(url_for('admin'))
    return render_template('login.html')



def insert_sorted(session_list, new_session):
    """
    Вставляет новый предмет в отсортированный порядок в списке предметов.
    """
    for index, session in enumerate(session_list):
        if datetime.strptime(session['start_time'], '%H:%M') > datetime.strptime(new_session['start_time'], '%H:%M'):
            session_list.insert(index, new_session)
            return
    session_list.append(new_session)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        day = get_day_of_week(request.form['date'])
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        subject = request.form['subject']
        date = request.form['date']
        new_session = {
                'start_time': start_time,
                'end_time': end_time,
                'subject': subject,
                'date': date
            }
        if day in schedule:
                insert_sorted(schedule[day], new_session)
        else:
            schedule[day] = [new_session]

    return render_template('admin.html', schedule=schedule)

@app.route('/delete/<day>/<index>')
def delete(day, index):
    index = int(index)
    if day in schedule and 0 <= index < len(schedule[day]):
        del schedule[day][index]
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
