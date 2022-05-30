# import library
from tokenize import Name
from flask import Flask, flash, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
# init main app
app = Flask(__name__)
# kunci rahasia agar session bisa berjalan
app.secret_key = '!@#$%'


# database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prak_9'
# init mysql
mysql = MySQL(app)


# set route default dan http method yang dizinkan     route ‘/’
@app.route('/', methods=['GET', 'POST'])
# function login
def awal():
    global email
    # cek jika method POST dan ada form data maka proses login
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form:
        # buat variabel untuk memudahkan pengolahan data
        email = request.form['inpEmail']
        passwd = request.form['inpPass']
        # cursor koneksi mysql
        cur = mysql.connection.cursor()
        # eksekusi kueri
        cur.execute(
            "SELECT * FROM data where email = %s and password = %s", (email, passwd))
        # fetch hasil kueri
        result = cur.fetchone()
        # cek hasil kueri
        if result:
            # jika login valid buat data session
            session['is_logged_in'] = True
            session['username'] = result[1]
            # Redirect ke halaman home
            return redirect(url_for('home'))
        else:
            # jika login invalid kembalikan ke login form
            return render_template('erorpage.html')
    else:
        # jika method selain POST tampilkan form login
        return render_template('login.html')

# route sign in

@app.route('/login', methods=['GET', 'POST'])
# function login
def login():
    global email
    # cek jika method POST dan ada form data maka proses login
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form:
        # buat variabel untuk memudahkan pengolahan data
        email = request.form['inpEmail']
        passwd = request.form['inpPass']
        # cursor koneksi mysql
        cur = mysql.connection.cursor()
        # eksekusi kueri
        cur.execute(
            "SELECT * FROM data where email = %s and password = %s", (email, passwd))
        # fetch hasil kueri
        result = cur.fetchall()
        # cek hasil kueri
        if result:
            # jika login valid buat data session
            session['is_logged_in'] = True
            session['username'] = result[0][1]
            session['level'] = result[0][4]
            # print(result[0]);
            # return session['level']
            # Redirect ke halaman home
            return redirect(url_for('adminhome'))
        else:
            # jika login invalid kembalikan ke login form
            return render_template('indexhome.html')
    else:
        # jika method selain POST tampilkan form login
        return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    # cek session apakah sudah login
    if 'is_logged_in' in session:
        # # cursor koneksi mysql
        # cur = mysql.connection.cursor()
        # # eksekusi kueri
        # cur.execute(f"SELECT * FROM data where email = '{email}'")
        # # fetch hasil kueri
        # feri = cur.fetchall()
        # # tutup koneksi
        # cur.close()
        # render data bersama template
        return render_template('indexhome.html')
    else:
        return redirect(url_for('eror'))

        # route logout

@app.route('/adminhome')
def adminhome():
    # hapus data session session.pop('is_logged_in', None) session.pop('username', None)
    # Redirect to login page
    return render_template('/layout/index.html')
    # debug dan auto reload

@app.route('/tables')
def table():
    # hapus data session session.pop('is_logged_in', None) session.pop('username', None)
    # Redirect to login page
    return render_template('tables.html')
    # debug dan auto reload


# @app.route('/register')
# def regist():
    
#     # Redirect to login page
#     return render_template('register.html')
#     # debug dan auto reload


@app.route('/logout')
def logout():
    
    # Redirect to login page
    return render_template('login.html')
    # debug dan auto reload


@app.route('/eror')
def eror():
   
    # Redirect to login page
    return render_template('404.html')
    # debug dan auto reload


@app.route('/form')
def form():
    
    # Redirect to login page
    return render_template('form.html')
    # debug dan auto reload


@app.route('/contact')
def contact():
    
    # Redirect to login page
    return render_template('contact.html')
    # debug dan auto reload

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'namane' in request.form and 'emaile' in request.form and 'Passworde' in request.form :
        username = request.form['namane']
        password = request.form['Passworde']
        email = request.form['emaile']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM data WHERE Username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO data (Username,password,email) VALUES ( % s, % s, % s)', (username,password,email ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    else:
         return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
