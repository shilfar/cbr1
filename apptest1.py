#!/usr/bin/python3

from flask import Flask, render_template, request, url_for, redirect
import os
import random
from tabulate import tabulate
import psycopg2

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(database="mytestdb", user='postgres', password='u20', host='1.1.1.90', port='5432')
    conn.autocommit = True
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
#    conn = psycopg2.connect(database="mytestdb", user='postgres', password='ubuntu20', host='192.168.1.90', port='5432')
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT * FROM exchange_rate")
#    cur.execute("SELECT * FROM exchange_rate WHERE Date = '03/03/2022' ORDER BY Name ASC")
    rows = cur.fetchall()
    columns = ['date', 'id', 'numcode', 'charcode', 'nominal', 'name', 'value']
    print(tabulate(rows, headers=columns, tablefmt='html', stralign='center'))
    valute_table = tabulate(rows, headers=columns, tablefmt='html')
    report = open('/docker-flask-test/templates/valute.html', 'w')
    report.write(valute_table)
    report.close()
    cur.close()
    conn.close()
    return render_template('valute.html')

@app.route('/check/', methods=('GET', 'POST'))
def check():
    if request.method == 'POST':
        date_req = request.form['date_req']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM exchange_rate WHERE Date = %s ORDER BY Name ASC", [date_req])
        rows = cur.fetchall()
        columns = ['date', 'id', 'numcode', 'charcode', 'nominal', 'name', 'value']
        print(tabulate(rows, headers=columns, tablefmt='html', stralign='center'))
        valute_table = tabulate(rows, headers=columns, tablefmt='html')
        report = open('/docker-flask-test/templates/valute_3.html', 'w')
        report.write(valute_table)
        report.close()
        cur.close()
        conn.close()

    return render_template('index.html')

@app.route('/valute')
def valute():
    return render_template('valute_3.html')

# @app.route('/')
# def hello_world():
#     return render_template('index.html')

if __name__ == "__main__":
#     app.run()
#    app.run(debug=True)
    app.run(debug=True,host='0.0.0.0')
