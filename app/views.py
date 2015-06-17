from app import app
from flask import render_template
import urllib

@app.route('/')
@app.route('/index')
def index():
    state_bed1 = urllib.urlopen('http://192.168.1.101/cgi-bin/relay.cgi?state').read()
    return render_template('index.html', title='Home', state_bed1=state_bed1)

@app.route('/test')
def test():
    return render_template('test.html', title='test')