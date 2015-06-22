from app import app, db
from flask import render_template, redirect, request
import urllib
from .models import devices, timer

@app.route('/')
@app.route('/index')
def index():
    bed1_initial_class="btn-danger"
    state_bed1 = urllib.urlopen('http://192.168.1.101/cgi-bin/relay.cgi?state').read()
    state_bed1 = state_bed1.strip()
    if state_bed1 == "ON":
        bed1_initial_class="btn-success"
    datimers = timer.query.all()

    return render_template('index.html', title='Home',
                                         timer = datimers,
                                         bed1_initial_class=bed1_initial_class,
                                         state_bed1=state_bed1)

@app.route('/add_timer', methods=['POST'])
def add_timer():
    start=request.form['starttime']
    end=request.form['endtime']
    #start = float(start)/4.0
    #end = float(end)/4.0
    newtimer = timer()
    newtimer.name_id = 1
    newtimer.start_time = start
    newtimer.end_time = end
    db.session.add(newtimer)
    db.session.commit()
    #flash('Entry was deleted')
    return redirect('/index')
    #return render_template('delete.html', title='Home', starter=start, ender=end)

@app.route('/delete_timer/<postID>', methods=['POST'])
def delete_timer(postID):
    timer.query.filter(timer.id == postID).delete()
    db.session.commit()
    #flash('Entry was deleted')
    return redirect('/index')

@app.route('/testbed2')
def test():
    return render_template('testbed2.html', title='testbed2')
