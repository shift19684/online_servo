from flask import Flask
print(Flask(__name__))
from flask import render_template
from flask import request
import subprocess

app = Flask(__name__)


subprocess.run(['sudo', 'tc', 'qdisc', 'add', 'dev', 'wlan1', 'root', 'netem','delay', '0ms', 'loss', '0%', 'duplicate', '0%'])




@app.route('/', methods=['GET', 'POST'])
def index():

	if request.method == 'GET':
		sReqDelay = 'delayNone'
		sReqLoss = 'lossLess'
		sReqControll = 'controllNone'
		sReqComm = 'commNone'

	if request.method == 'POST':
		sReqDelay = request.form["delay"]
		sReqLoss = request.form["loss"]
		sReqControll = request.form["controll"]
		sReqComm = request.form["comm"]

		sNumDelay = '0ms'
		match sReqDelay:
			case 'delay0s':
				sNumDelay = '0ms'
			case 'delay1ds':
				sNumDelay = '100ms'
			case 'delay2ds':
				sNumDelay = '200ms'	
			case 'delay4ds':
				sNumDelay = '400ms'
			case 'delay5ds':
				sNumDelay = '500ms'
			case 'delay6ds':
				sNumDelay = '600ms'
			case 'delay8ds':
				sNumDelay = '800ms'					
			case 'delay1s':
				sNumDelay = '1000ms'
			case 'delay2s':
				sNumDelay = '2000ms'
			case 'delay3s':
				sNumDelay = '3000ms'
			case 'delay4s':
				sNumDelay = '4000ms'
			case 'delay5s':
				sNumDelay = '5000ms'	
			case 'delay6s':
				sNumDelay = '6000ms'
			case 'delay7s':
				sNumDelay = '7000ms'	
			case 'delay8s':
				sNumDelay = '8000ms'
			case 'delay9s':
				sNumDelay = '9000ms'
			case 'delay10s':
				sNumDelay = '10000ms'
			case 'delay11s':
				sNumDelay = '11000ms'	
			case 'delay12s':
				sNumDelay = '12000ms'
			case 'delay13s':
				sNumDelay = '13000ms'	
			case 'delay14s':
				sNumDelay = '14000ms'
			case 'delay15s':
				sNumDelay = '15000ms'	
			case 'delay16s':
				sNumDelay = '16000ms'
			case 'delay17s':
				sNumDelay = '17000ms'	
			case 'delay18s':
				sNumDelay = '18000ms'
			case 'delay19s':
				sNumDelay = '19000ms'							
			case 'delay20s':
				sNumDelay = '20000ms'
			case 'delay21s':
				sNumDelay = '21000ms'	
			case 'delay22s':
				sNumDelay = '22000ms'
			case 'delay23s':
				sNumDelay = '23000ms'	
			case 'delay24s':
				sNumDelay = '24000ms'		
			case 'delay25s':
				sNumDelay = '25000ms'
			case 'delay26s':
				sNumDelay = '26000ms'
			case 'delay27s':
				sNumDelay = '27000ms'
			case 'delay28s':
				sNumDelay = '28000ms'
			case 'delay29s':
				sNumDelay = '29000ms'
			case 'delay30s':
				sNumDelay = '30000ms'
			case 'delay40s':
				sNumDelay = '40000ms'				
			case 'delay50s':
				sNumDelay = '50000ms'
			case 'delay60s':
				sNumDelay = '60000ms'
			case 'delay70s':
				sNumDelay = '70000ms'
			case 'delay80s':
				sNumDelay = '80000ms'
			case 'delay90s':
				sNumDelay = '90000ms'
			case _:
				sNumDelay = '0ms'

		sNumLoss = '0%'
		match sReqLoss:
			case 'lossLess':
				sNumLoss = '0%'
			case 'lossLow':
				sNumLoss = '3%'
			case 'lossMiddle':
				sNumLoss = '10%'
			case 'lossHigh':
				sNumLoss = '30%'
			case 'lossHigher':
				sNumLoss = '40%'
			case 'lossHuge':
				sNumLoss = '60%'
			case _:
				sNumLoss = '0%'


		subprocess.run(['tc', 'qdisc', 'del', 'dev', 'wlan1', 'root'])

		subprocess.run(['tc', 'qdisc', 'add', 'dev', 'wlan1', 'root', 'netem','delay', sNumDelay, 'loss', sNumLoss, 'duplicate', sNumLoss])
		
		
		if sReqControll == 'controllReboot':
				subprocess.run(['sudo', 'reboot'])
				return '<html><body><h1> Rebooting now </h1></body></html>'
		


		if sReqControll == 'controllShutdown':
				subprocess.run(['shutdown', '-h', '+0'])
				return '<html><body><h1> Shutdown after 1 min </h1></body></html>'
		

		if sReqComm == 'commStop':
			subprocess.run(["sudo", "nft", "add", "table", "ip", "simulate_drop"])
			subprocess.run(["sudo", "nft", "add", "chain", "ip", "simulate_drop", "my_forward", "{ type filter hook forward priority 0; policy accept; }"])
			subprocess.run(["sudo", "nft", "add", "rule", "ip", "simulate_drop", "my_forward", "iifname", "wlan1", "reject", "with", "icmp", "type", "host-unreachable"])
			sNumDelay = 'S'
			sNumLoss = 'S'


		if sReqComm == 'commRecover':
			subprocess.run(["sudo", "nft", "delete", "table", "ip", "simulate_drop"])
			sNumDelay = 'R'
			sNumLoss = 'R'


		subprocess.run(['/home/sudox/tvo/tv01/bin/python', '/home/sudox/tvo/tv01/tv01.py', sNumDelay, sNumLoss])



	return makePage(sReqDelay, sReqLoss, sReqComm)


def makePage(vDelay, vLoss, vComm):
	return render_template('changesettings.html', DelayValue=vDelay, LossValue=vLoss, CommValue=vComm)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)


