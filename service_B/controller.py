from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_mysqldb import MySQL
from config import host, user, password, db_name
import os
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, send, emit

# Настройка загрузки файлов 1
UPLOAD_FOLDER = 'C:/Users/jisca/Desktop/diplom/plc'
UPLOAD_FOLDER1 = 'C:/Users/jisca/Desktop/diplom/check_list'
UPLOAD_FOLDER2 = 'C:/Users/jisca/Desktop/diplom/documentation'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
# активируем socketIO
socketio = SocketIO(app)

# Устанавливаем SECREt KEY
app.config['SECRET_KEY'] = '>gfhf89dx,v06kdgfh78@#5'

# Настройка загрузки файлов 2
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2

# Подключаемся к базе данных
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = db_name
mysql = MySQL(app)

# Пишем словарь для отображения меню приложения
menu = [{"name": "Список оборудования", "url": "/"},
        {"name": "Рекламации", "url": "list-request"},
        {"name": "Заказчики", "url": "customers"},
        {"name": "ПНР", "url": "comissioning"},
        {"name": "Статистика", "url": "statistics"},
        {"name": "Помощь", "url": "about"}]


# Настройка загрузки файлов 3
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('index.html', menu=menu)


@app.route("/list-request", methods=['GET', 'POST'])
def list_request():
    return render_template('list-request.html', menu=menu)


@app.route("/comissioning")
def comissioning():
    return render_template('comissioning.html', menu=menu)


@app.route("/customers")
def customers():
    return render_template('customers.html', menu=menu)


@app.route("/statistics")
def statistics():
    return render_template('statistics.html', menu=menu)


@app.route("/create_cnc", methods=['POST', 'GET'])
def create_cnc():
    if request.method == 'POST':
        typ_eq = request.form['typ_eq']
        model = request.form['model']
        ser_number = request.form['ser_number']
        cnc_typ = request.form['cnc_typ']
        # создаем курсор для взаимодействия с БД (сканировать/запрашивать/удалять)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO equipment(typ_eq,model,ser_number,cnc_typ) VALUES (%s, %s, %s, %s)",
                    (typ_eq, model, ser_number, cnc_typ))
        mysql.connection.commit()
        cur.close()
        print(request.form)
        # f = request.files['file']
        # f.save(f"{secure_filename(f.filename)}")
        # if 'plc' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        file = request.files['plc']
        file1 = request.files['check_list']
        file2 = request.files['docs']
        # file1 = request.files['check_list']
        # file2 = request.files['docs']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index', name=filename))

        if file1 and allowed_file(file1.filename):
            filename = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
            return redirect(url_for('index', name=filename))

        if file2 and allowed_file(file2.filename):
            filename = secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
            return redirect(url_for('index', name=filename))
    return render_template('create_cnc.html')


@app.route("/create_customer", methods=['POST', 'GET'])
def create_customer():
    if request.method == 'POST':
        organization = request.form['organization']
        adress = request.form['adress']
        email = request.form['email']
        phone = request.form['phone']
        contract = request.form['contract']
        statistic = request.form['statistics_idstatistics']
        # создаем курсор для взаимодействия с БД (сканировать/запрашивать/удалять)
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO customer(organization,adress,email,phone,contract, statistics_idstatistics) VALUES (%s, %s, %s, %s, %s, %s)",
            (organization, adress, email, phone, contract, statistic))
        mysql.connection.commit()
        cur.close()

        name_cust = request.form['name_cust']
        lastname = request.form['lastname']
        surname = request.form['surname']
        phone_cust = request.form['phone_cust']
        position_cust = request.form['position_cust']
        cust_idcust = request.form['customer_idcustomer']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO customer_contact(name_cust,lastname,surname,phone_cust,position_cust, customer_idcustomer) VALUES (%s, %s, %s, %s, %s,%s)",
            (name_cust, lastname, surname, phone_cust, position_cust, cust_idcust))
        mysql.connection.commit()
        cur.close()
        print(request.form)
    return render_template('create_customer.html')


@app.route("/about")
def about():
    return render_template('about.html', title="Как пользоваться", menu=menu)


# @app.route("/profile/<username>")
# def profile(username):
#     return f"Пользователь: {username}"
#
#
# with app.test_request_context():
#     print(url_for('create_cnc'))

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu)


@socketio.on('message')
def message(data):
    # print(f"\n\n{data}\n\n")
    send(data)
    # emit('some-event', 'this is a custom event message')


if __name__ == '__main__':
    app.run(debug=True)
