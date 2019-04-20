from flask import render_template, flash, redirect, request, jsonify
from flask import current_app as app
from app.forms import LoginForm
import sqlite3 as sql
from datetime import datetime
from time import strftime


@app.route('/old')
def index():
	#return app.send_static_file('main.html')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/sensor')
def sensor():
    return render_template('base.html')


@app.route('/addtemp', methods = ['POST', 'GET'])
def addTemp():
    if request.method == 'GET':#'POST':
        try:
            now = datetime.now()
            date = now.strftime('%Y-%m-%d')
            time = now.strftime('%H:%M:%S')
            temp = request.args['temp']
            hum = request.args['hum']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO temperature (date, time, temperature, humidity)   \
                    VALUES ('{}', '{}', {}, {})".format(date, time, temp, hum))
                
                con.commit()
                msg = "Record successfully added"

                con.close()
        except:
            msg = "error in insert operation"
            print('ERROR')
        finally:
            return render_template("result.html", msg = msg)


@app.route('/adddist', methods = ['POST', 'GET'])
def addDist():
    if request.method == 'GET':#'POST':
        try:
            now = datetime.now()
            date = now.strftime('%Y-%m-%d')
            time = now.strftime('%H:%M:%S')
            dist = request.args['dist']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO distance (date, time, distance)   \
                    VALUES ('{}', '{}', {})".format(date, time, dist))
                
                con.commit()
                msg = "Record successfully added"

                con.close()
        except:
            msg = "error in insert operation"
            print('ERROR')
        finally:
            return render_template("result.html", msg = msg)


@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from temperature")
   tempRows = cur.fetchall()

   cur.execute("select * from distance")
   distRows = cur.fetchall()
   
   return render_template("results.html", tempRows=tempRows, distRows=distRows)


@app.route('/gettemp')
def getTemp():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
   
    cur = con.cursor()
    cur.execute("select * from temperature")
    tempRows = cur.fetchall()

    data = []
    for row in tempRows:
        data.append(dict(row))

    return jsonify(data)


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)