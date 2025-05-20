from flask import *
import requests
from wifiscan import *

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/networks')
def networks():
	return jsonify(scan_wifi())
	
@app.route('/connect', methods=['POST'])
def connect():
	ssid=request.form.get('ssid')
	password=request.form.get('password')
	if connect_wifi(ssid, password):
		return 'Success'
	else:
		return 'Fail', 400
		
@app.route('/wifiname')
def wifiname():
	ssid=get_connected_ssid()
	if ssid is not None:
		return ssid
	return 'Fail', 400
	
@app.route('/marconn')
def marconn():
	return requests.get('http://localhost:8000/active').text
	
if __name__=='__main__':
	app.run('0.0.0.0', 5000)