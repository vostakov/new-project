from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = '123kjbsfdfskjfbk1'
# Пример расписания в виде словаря (в реальном приложении данные следует хранить в базе данных).
schedule = {}

sch = { '09:00':['1','2','09:00','09:45','09:45','10:35' ], 
       '10:45':['3','4','10:45', '11:30','11:35','12:20'],
       '13:00':['5','6','13:00', '13:45', '13:50','14:35'],
       '14:45':['7','8', '14:45', '15:30' ,'15:35' , '16:20' ]
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

    # Переводим выбранную дату в день недели
    selected_day = get_day_of_week(selected_date)

    # Если для выбранного дня есть расписание, используем его. Иначе, используем пустой список.
    day_schedule = schedule.get(selected_day, [])

    return render_template('index.html', schedule=day_schedule, selected_date=selected_date, selected_day=selected_day)

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
        date = request.form.get('date')


        # Проверка наличия всех обязательных полей
        if date:
            # Ваш код обработки формы
            day = get_day_of_week(date)
            start_time = request.form['start_time']
            subject = request.form['subject']
            if start_time in sch:
                new_session = {
                'n_lesson': sch[start_time][0],
                'start_time': sch[start_time][2],
                'end_time':  sch[start_time][3],
                'subject': subject,
                'date': date
                }
                new_sesion1 = {
                'n_lesson': sch[start_time][1],
                'start_time': sch[start_time][4],
                'end_time': sch[start_time][5],
                'subject': subject,
                'date': date
                }
                if day in schedule:
                    insert_sorted(schedule[day], new_session)
                    insert_sorted(schedule[day], new_sesion1)
                else:
                    schedule[day] = [new_session,new_sesion1]
            flash('Сессия успешно добавлена', 'success')
            return redirect(url_for('admin_success'))
            return render_template('admin.html', schedule=schedule)


        else:
            flash('Ошибка: Не все данные формы были предоставлены', 'error')

    return render_template('admin.html', schedule=schedule)



@app.route('/admin_success')
def admin_success():
    # Сюда можно добавить дополнительные действия, если необходимо
    return render_template('admin_success.html')



@app.route('/delete/<day>/<index>')
def delete(day, index):
    index = int(index)
    if day in schedule and 0 <= index < len(schedule[day]):
        del schedule[day][index]
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
