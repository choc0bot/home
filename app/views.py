from app import app, db
from flask import render_template, redirect, request, flash, jsonify
import urllib2
from .models import devices, timer, log
from time import strftime
from datetime import datetime, timedelta
import temperature
#from datetime import datetime

def write_log(deviceid, state):
    newlog = log()
    newlog.devices_id = deviceid
    newlog.state = state
    newlog.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.session.add(newlog)
    db.session.commit()    

def check_status(deviceip):
    status_url = "http://" + deviceip + "/cgi-bin/relay.cgi?state"
    try:
        status_check = urllib2.urlopen(status_url, timeout=0.2).read()
        status = status_check.strip()
    except:
        status = "OFF"
    return status

def turn_on(deviceip, deviceid):
    on_url = "http://" + deviceip + "/cgi-bin/relay.cgi?on"
    try:
        on_check = urllib2.urlopen(on_url, timeout=0.1).read()
        on_status = on_check.strip()
        write_log(deviceid, check_status(deviceip))
    except:
        on_status = "OFF"
    return on_status

def turn_off(deviceip, deviceid):
    off_url = "http://" + deviceip + "/cgi-bin/relay.cgi?off"
    try:
        off_check = urllib2.urlopen(off_url, timeout=0.3).read()
        off_status = off_check.strip()
        write_log(deviceid, check_status(deviceip))
    except:
        off_status = "OFF"
    return off_status


def toggle_device(deviceip, deviceid):
    toggle_url = "http://" + deviceip + "/cgi-bin/relay.cgi?toggle"
    try:
        toggle_check = urllib2.urlopen(toggle_url, timeout=0.3).read()
        toggle_status = toggle_check.strip()
        write_log(deviceid, check_status(deviceip))
    except:
        toggle_status = "NA"
    return toggle_status

@app.route('/toggle')
def toggle():
    deviceip = request.args.get('deviceip')
    deviceid = request.args.get('deviceid')
    status = toggle_device(deviceip, deviceid)
    return status


@app.route('/index-bs')
def indexbs():
    #state_bed1 = urllib2.urlopen('http://192.168.1.101/cgi-bin/relay.cgi?state').read()
    datimers = timer.query.all()
    dadevices = devices.query.all()
    device_status_list = []
    cur_temp = str(round(temperature.read_temp(),1))
    for check_devices in dadevices:
        state_bed1 = check_status(check_devices.ip)
        state_bed1 = state_bed1.strip()
        if state_bed1 == "ON":
            button_status="btn-success"
        else:
            button_status="btn-danger"
        device_status_list.append([check_devices.id, check_devices.name, button_status, check_devices.ip, check_devices.temp])

    return render_template('index-bs.html', title='Home',
                                         device_list = device_status_list,
                                         timer = datimers,
                                         cur_temp = cur_temp,
                                         state_bed1=state_bed1)
@app.route('/')
@app.route('/index')
def index():
    #state_bed1 = urllib2.urlopen('http://192.168.1.101/cgi-bin/relay.cgi?state').read()
    datimers = timer.query.all()
    dadevices = devices.query.all()
    device_status_list = []
    cur_temp = str(round(temperature.read_temp(),1))
    for check_devices in dadevices:
        state_bed1 = check_status(check_devices.ip)
        state_bed1 = state_bed1.strip()
        if state_bed1 == "ON":
            button_status="mdl-color--green-300"
        else:
            button_status="mdl-color--red-300"
        device_status_list.append([check_devices.id, check_devices.name, button_status, check_devices.ip, check_devices.temp])

    return render_template('index.html', title='Home',
                                         device_list = device_status_list,
                                         timer = datimers,
                                         cur_temp = cur_temp,
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
    if end == '24:00':
        end = '00:00'
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

@app.route('/add_temp', methods=['POST'])
def add_temp():
    """
    Retrieves input form and writes to the db
    """
    temperature = request.form['temperature']
    deviceid = request.form['deviceid']

    device = devices.query.get(deviceid)
    device.temp = temperature
    db.session.commit()
    #flash('Entry was added')
    return redirect('/index')

@app.route('/check_device_status', methods=['POST'])
def check_device_status():
    deviceid = request.form['deviceid']
    device = devices.query.get(deviceid)
    state = check_status(device.ip)
    return jsonify(staus=state)

@app.route('/check_temp', methods=['POST'])
def check_temp():
    cur_temp = str(round(temperature.read_temp(),1))
    return jsonify(temp=cur_temp)

@app.route('/check_timers')
def check_timers():
    flag = "NO"
    deviceip="notset"
    cur_time = strftime("%H:%M")
    datimers = timer.query.all()
    dastatus = check_status("192.168.1.101")
    testlist = []
    #maxtemp = 23
    for timer_entry in datimers:
        deviceip=devices.query.filter_by(id=timer_entry.name_id).first().ip
        maxtemp=float(devices.query.filter_by(id=timer_entry.name_id).first().temp)
        if maxtemp == 0.0:
            maxtemp=99
        if timer_entry.start_time < cur_time and timer_entry.end_time > cur_time and temperature.read_temp() < maxtemp:
            if check_status(deviceip) =="OFF":
                turn_on(deviceip, timer_entry.name_id)
        #teststatus = "OFF"
        testv = datetime.strptime(cur_time, '%H:%M') - datetime.strptime(timer_entry.end_time, '%H:%M')
        if testv > timedelta(minutes=1) and testv < timedelta(minutes=5) or temperature.read_temp() > maxtemp:
            flag = "YES " + str(testv) + " " + (deviceip)
            if check_status(deviceip) == "ON":
                turn_off(deviceip, timer_entry.name_id)
            if testv > timedelta(minutes=1) and timer_entry.timer_type == 0:
                delete_timer(timer_entry.id)
        #time.strptime(stamp, '%I:%M')
        teststatus = check_status(deviceip)
        testlist.append([timer_entry.name_id,timer_entry.start_time,timer_entry.end_time,teststatus,testv,maxtemp])

    return render_template('test.html', time=cur_time,
                                        status=dastatus,
                                        flag=flag,
                                        testv=testv,
                                        testc=timedelta(minutes=1),
                                        timers=testlist)


@app.route('/log')
def test():
    dalog = log.query.all()
    dadevices = devices.query.all()
    log_list = []
    for device in dadevices:
        off_count = 0
        on_count = 0
        total_time = 0
        for entry in dalog:            
            if entry.devices_id == device.id:
                if entry.state == "ON":
                    on_count += 1
                    on_time = datetime.strptime(entry.time, '%Y-%m-%d %H:%M:%S')
                    #log_list.append([entry.devices_id, entry.state, entry.time])
                if entry.state == "OFF":
                    off_count += 1
                    accrued_time = datetime.strptime(entry.time, '%Y-%m-%d %H:%M:%S') - on_time
                    if accrued_time.total_seconds() < 0:
                        accrued_time = 0
                    else:
                        accrued_time = accrued_time.total_seconds()
                    total_time = total_time + accrued_time
        log_list.append([device.id, on_count, off_count, total_time/3600])
    return render_template('testbed2.html', title='testbed2',
                                            log = log_list)
