import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# create application
reqapp = Flask(__name__)
reqapp.config.from_object(__name__)

#Load configurations
reqapp.config.update(dict(
    DATABASE=os.path.join(reqapp.root_path, 'request_repo.db'),
    SECRET_KEY='key',
    USERNAME='admin',
    PASSWORD='default'
))
reqapp.config.from_envvar('FLASKR_SETTINGS', silent=True)

def conn_db():
    rv = sqlite3.connect(reqapp.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
	g.sqlite_db = conn_db()
    return g.sqlite_db

@reqapp.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
	g.sqlite_db.close()

def init_db():
    db = get_db()
    with reqapp.open_resource('schema.sql', mode='r') as f:
	db.cursor().executescript(f.read())
    db.commit()

@reqapp.cli.command('initdb')
def initdb_command():
    init_db()
    print 'Database Initialized.'

@reqapp.route('/')
def show_requests():
    db = get_db()
    req = db.execute('select reqid, title, description, client, priority, target_date, ticket_url, product_area from requests')
    requests = req.fetchall()
    return render_template('show_requests.html', requests=requests)

@reqapp.route('/add', methods=['POST'])
def add_request():
    if not session.get('logged_in'):
	abort(401)
    db = get_db()
    db.execute('insert into requests (title, description, client, priority, target_date, ticket_url, product_area) values (?, ?, ?, ?, ?, ?, ?)', [request.form['title'], request.form['description'], request.form['client'], request.form['priority'], request.form['target_date'], request.form['ticket_url'], request.form['product_area']])
    db.commit()
    flash('Request successfully submitted')
    return redirect(url_for('show_requests'))

@reqapp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
	if request.form['username'] != reqapp.config['USERNAME']:
	    error = 'Wrong User'
	elif request.form['password'] != reqapp.config['PASSWORD']:
	    error = 'Wrong Password'
	else:
	    session['logged_in'] = True
	    flash('You have been logged in')
	    return redirect(url_for('show_requests'))
    return render_template('login.html', error=error)

@reqapp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out')
    return redirect(url_for('show_requests'))
