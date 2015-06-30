from app import app, db
from flask import render_template, redirect, request, flash
import urllib2
from .models import devices, timer
from time import strftime
import datetime

def check_status(deviceip):
    status_url = "http://" + deviceip + "/cgi-bin/relay.cgi?state"
    try:
        status_check = urllib2.urlopen(status_url, timeout=0.2).read()
        status = status_check.strip()
    except:
        status = "OFF"
    return status

def turn_on(deviceip):
    on_url = "http://" + deviceip + "/cgi-bin/relay.cgi?state"
    on_check = urllib2.urlopen(on_url).read()
    on_status = on_check.strip()
    return on_status

@app.route('/')
@app.route('/index')
def index_new():
    #state_bed1 = urllib2.urlopen('http://192.168.1.101/cgi-bin/relay.cgi?state').read()
    datimers = timer.query.all()
    dadevices = devices.query.all()
    device_status_list = []
    for check_devices in dadevices:
        state_bed1 = check_status(check_devices.ip)
        state_bed1 = state_bed1.strip()
        if state_bed1 == "ON":
            button_status="btn-success"
        else:
            button_status="btn-danger"
        device_status_list.append([check_devices.id, check_devices.name, button_status, check_devices.ip])

    return render_template('index.html', title='Home',
                                         device_list = device_status_list,
                                         timer = datimers,
                                         state_bed1=state_bed1)

@app.route('/add_timer', methods=['POST'])
def add_timer():
    """
    Retrieves input form and writes to the db
    """
    start = request.form['starttime']
    end = request.form['endtime']
    nameid = request.form['deviceid']
    timertype = request.form['timertype']
    newtimer = timer()
    newtimer.name_id = nameid
    newtimer.start_time = start
    newtimer.end_time = end
    newtimer.timer_type = timertype
    db.session.add(newtimer)
    db.session.commit()
    #flash('Entry was added')
    return redirect('/index')
    #return render_template('delete.html', title='Home', starter=start, ender=end)

@app.route('/delete_timer/<postID>', methods=['POST'])
def delete_timer(postID):
    timer.query.filter(timer.id == postID).delete()
    db.session.commit()
    return redirect('/index')

@app.route('/check_timers')
def check_timers():
    set_timer="notset"
    deviceip="notset"
    cur_time = strftime("%H:%M")
    datimers = timer.query.all()
    dastatus = check_status("192.168.1.101")
    for timer_entry in datimers:
        if timer_entry.start_time < cur_time and timer_entry.end_time > cur_time:
            deviceip=devices.query.filter_by(id=timer_entry.name_id).first().ip
            set_timer="ON"
            if check_status(deviceip) =="OFF":
                turn_on(deviceip)

    return render_template('test.html', time=cur_time,
                                        timer_set=set_timer,
                                        device=deviceip,
                                        status=dastatus)


@app.route('/testbed2')
def test():
    return render_template('testbed2.html', title='testbed2')
