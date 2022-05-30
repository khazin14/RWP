from flask import Flask, flash, render_template, request, redirect, session, url_for
import random

app = Flask(__name__)
app.secret_key = "0askmFaeu1"  


import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "pbop-kelompok"
)
cursor = db.cursor()

@app.route("/")
def index():
    return render_template('login.html')


@app.route("/login", methods = ['POST'])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    # di cek dari daabase, apakah data user dengan username dan pasword tersebut ada?
    sql = f'select * from user where username = "{username}" and password = "{password}"'
    cursor.execute(sql)
    data = cursor.fetchall()
    if data == [] :
        return render_template('login.html', pesan = 'Username dan Password Anda salah!')
    else :
    # jika ada dilanjutkan ke rout('dashboard)
        session['nama'] = data[0][1]
        session['rule'] = data[0][6]
        session['id'] = data[0][0]
        # print(data[0][1])
        return redirect(url_for('dashboard'))
    
@app.route('/logout')
def logout():
    session.pop('nama', None)
    return redirect(url_for('/'))




@app.route("/dashboard")
def dashboard():
    # cursor.execute('select count(*) from mahasiswa')
    # jumlah_mahasiswa = 
    # jumlah_dosen =
    # jumlah_matkul = 

    return render_template('dashboard.html')


# master data dosen

# index
@app.route("/dosen")
def dosen():
    sql = 'select * from dosen'
    cursor.execute(sql)
    data = cursor.fetchall()

    return render_template('dosen/index.html', data = data)


# tambah data
@app.route("/dosen/create")
def tambah_dosen():
    return render_template('dosen/create.html')

@app.route('/dosen/store', methods = ['POST'])
def store_dosen() :
    
    nama = request.form.get("nama")
    nidn = request.form.get("nidn")
    prodi = request.form.get("prodi")

    sql = f"INSERT INTO `dosen`(`nama`, `nidn`, `prodi`) VALUES ('{nama}','{nidn}','{prodi}')"
    cursor.execute(sql)
    db.commit()

    return redirect(url_for('dosen'))

# edit
@app.route('/dosen/edit/<id>')
def edit_dosen(id) :
    id = id

    # ambil dulu data dosen yg mau diedit
    sql = f"select * from dosen where id = {id}"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data[0][0])
    return render_template('dosen/edit.html', data = data)


@app.route('/dosen/update/<id>', methods = ['POST'])
def update_dosen(id) :
    id = id

    nama = request.form.get("nama")
    nidn = request.form.get("nidn")
    prodi = request.form.get("prodi")

    sql = f"UPDATE `dosen` SET `nama`='{nama}',`nidn`='{nidn}',`prodi`='{prodi}' WHERE id = {id}"
    cursor.execute(sql)
    db.commit()

    return redirect(url_for('dosen'))

@app.route('/dosen/hapus/<id>')
def hapus_dosen(id):

    sql = f"DELETE FROM `dosen` WHERE id = {id}"
    cursor.execute(sql)    
    db.commit()

    return redirect(url_for('dosen'))

# end master data dosen

#master data mahasiswa


# index
@app.route("/mahasiswa")
def mahasiswa():
    sql = 'select * from mahasiswa'
    cursor.execute(sql)
    data = cursor.fetchall()

    return render_template('mahasiswa/index.html', data = data)


# tambah data

@app.route("/mahasiswa/create")
def tambah_mahasiswa():
    return render_template('mahasiswa/create.html')

@app.route('/mahasiswa/store', methods = ['POST'])
def store_mahasiswa() :
    
    nama = request.form.get("nama")
    nim = request.form.get("nim")
    angkatan = request.form.get("angkatan")

    sql = f"INSERT INTO `mahasiswa`(`nama`, `nim`, `angkatan`) VALUES ('{nama}','{nim}','{angkatan}')"
    cursor.execute(sql)
    db.commit()

    return redirect(url_for('mahasiswa'))


# edit data
@app.route('/mahasiswa/edit/<id>')
def edit_mahasiswa(id) :
    id = id

    # ambil dulu data mahasiswa yg mau diedit
    sql = f"select * from mahasiswa where id = {id}"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data[0][0])
    return render_template('mahasiswa/edit.html', data = data)

# Update data

@app.route('/mahasiswa/update/<id>', methods = ['POST'])
def update_mahasiswa(id) :
    id = id

    nama = request.form.get("nama")
    nim = request.form.get("nim")
    angkatan = request.form.get("angkatan")

    sql = f"UPDATE `mahasiswa` SET `nama`='{nama}',`nim`='{nim}',`angkatan`='{angkatan}' WHERE id = {id}"
    cursor.execute(sql)
    db.commit()

    return redirect(url_for('mahasiswa'))
# delete

@app.route('/mahasiswa/hapus/<id>')
def hapus_mahasiswa(id):

    sql = f"DELETE FROM `mahasiswa` WHERE id = {id}"
    cursor.execute(sql)    
    db.commit()

    return redirect(url_for('mahasiswa'))


# end master data mahasiswa



#master data matkul

# index
@app.route("/matkul")
def matkul():
    sql = 'select * from matkul'
    cursor.execute(sql)
    data = cursor.fetchall()

    return render_template('matkul/index.html', data = data)


# tambah data

@app.route("/matkul/create")
def tambah_matkul():
    return render_template('matkul/create.html')

@app.route('/matkul/store', methods = ['POST'])
def store_matkul() :
    
    kode = request.form.get("kode")
    nama  = request.form.get("nama")
    program_studi = request.form.get("program_studi")

    sql = f"INSERT INTO `matkul`(`kode`, `nama`, `program_studi`) VALUES ('{kode}','{nama}','{program_studi}')"
    cursor.execute(sql)
    db.commit()

    return redirect(url_for('matkul'))


# edit data
@app.route('/matkul/edit/<id>')
def edit_matkul(id) :
    id = id

    # ambil dulu data matkul yg mau diedit
    sql = f"select * from matkul wherelayo id = {id}"
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('matkul/edit.html', data = data)

# Update data

@app.route('/matkul/update/<id>', methods = ['POST'])
def update_matkul(id) :
    id = id

    kode = request.form.get("kode")
    nama = request.form.get("nama")
    prodi = request.form.get("prodi")

    sql = f"UPDATE `matkul` SET `kode`='{kode}',`nama`='{nama}',`prodi`='{prodi}' WHERE id = {id}"
    cursor.execute(sql)
    db.commit()

    return redirect(url_for('matkul'))
# delete

@app.route('/matkul/hapus/<id>')
def hapus_matkul(id):

    sql = f"DELETE FROM `matkul` WHERE id = {id}"
    cursor.execute(sql)    
    db.commit()

    return redirect(url_for('matkul'))

# end master data matkul




# KRS

# matkul krs
@app.route('/matkul-krs')
def matkul_krs():
    sql = 'select * from matkul'
    cursor.execute(sql)
    data = cursor.fetchall()

    return render_template('/krs/index.html', data = data)

# input krs
@app.route('/krs/store', methods = ['POST'])
def store_krs():
    mahasiswa_id = session['id']
    matkul = request.form.getlist("matkul[]")
    print(matkul)
    for item in matkul:
        sks = random.randint(1, 3)
        sql = f"INSERT INTO `krs`(`mahasiswa_id`, `matkul_id`, `sks`) VALUES ('{mahasiswa_id}','{item}','{sks}')"
        cursor.execute(sql)
        db.commit()


    return redirect((url_for('dashboard')))

# validasi krs
@app.route('/krs/validasi')
def validasi_krs():
    sql = '''SELECT krs.*, mahasiswa.*, matkul.* FROM krs 
            INNER JOIN mahasiswa ON   krs.mahasiswa_id=mahasiswa.id
            INNER JOIN matkul ON krs.matkul_id=matkul.id
            '''
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    return render_template('krs/validate.html', data = data)

@app.route('/krs/validasi/update/<mhs_id>', methods = ['POST'])
def update_validasi_kr(mhs_id):

    sql = f"UPDATE `krs` SET `status`='1' WHERE mahasiswa_id = {mhs_id}"
    cursor.execute(sql)
    db.commit()

    return redirect(url_for('dashboard'))


# cetak krs
@app.route('/krs/cetak')
def cetak_krs():

    sql = 'select * from krs'
    cursor.execute(sql) 
    data = cursor.fetchall()

    # jika status krs = 0 / belum di validasi dosen, maka tidak bisa cetak krs dulu
    if data[0][4] == 0 :
        flash("KRS belum acc DPA, belum bisa dicetak dulu brodayy")
        return redirect(url_for('dashboard'))
    else :
        return render_template('krs/cetak.html')


# END KRS


if __name__ == "__main__" :
    app.run(debug=True)
