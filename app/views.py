from app import app, db
from flask import render_template
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

@app.route('/testbed2')
def test():
    return render_template('testbed2.html', title='testbed2')
