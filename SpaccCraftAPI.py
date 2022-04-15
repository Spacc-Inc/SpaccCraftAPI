#!/usr/bin/env python3.8
""" ================================= |
| SpaccCraftAPI                       |
| Licensed under AGPLv3 by OctoSpacc  |
| ================================= """

import json
from flask import Flask, request, send_file
from APIConfig import *

app = Flask(__name__)

def MCAuth(User, Pass):
	with open(MCServerDir+'plugins/xAuth/auths.txt', 'r') as f:
		Users = f.readlines()
	for u in Users:
		ud = u.replace('\n','').split(':')
		if ud[0] == User and ud[1] == Pass:
			return True
	return False

def SubmitPoll(Ref, User, Vote):
	try:
		with open('APIDB.json', 'x') as f:
			f.close()
	except:
		pass

	try:
		with open('APIDB.json', 'r') as f:
			DBText = f.read()
		DB = json.loads(DBText) if DBText else {'Polls':{Ref:{User:''}}}
	except:
		return "Errore interno."

	if PollStarter and User != PollStarter and PollStarter not in DB['Polls'][Ref].keys():
		return "I voti non sono aperti."

	DB['Polls'][Ref][User] = Vote
	with open('APIDB.json', 'w') as f:
		json.dump(DB, f)
	return "Voto ({0}) salvato!".format(Vote) if Vote else "Voto ritirato!"

def HandlePost(Req):
	Data = Req.get_json()

	if not Data['Type'] or not Data['Ref']:
		return "Errore interno."
	if not Data['User'] or not Data['Pass']:
		return "Dati di accesso Mancanti, ricontrolla Username e Password!"
	if not MCAuth(Data['User'].lower(), Data['Pass']):
		return "Dati di accesso Errati, ricontrolla Username e Password!"

	if Data['Type'] == 'Poll':
		Vote = Data['Vote']
		if Vote == 'CustomText':
			Vote = Data['CustomText']
		return SubmitPoll(Data['Ref'], Data['User'].lower(), Vote)

@app.route('/Referendum/SpaccCraft-Video-Storia-20220415.html')
def SpaccCraftVideoStoria20220415():
	return send_file('Referendum/SpaccCraft-Video-Storia-20220415.html')

@app.route('/API', methods=['POST'])
def index():
	if request.method == 'POST':
		return HandlePost(request)

@app.route('/Style.css')
def SendCSS():
	return send_file('Style.css')

@app.route('/API.js')
def SendJS():
	return send_file('API.js')

@app.route('/Whirlpool.js')
def WhirlpoolJS():
	return send_file('Whirlpool.js')

if __name__ == '__main__':
	if Development:
		app.run(host='0.0.0.0', port=Port, debug=True) # wun with flask (development)
	else:
		from waitress import serve
		serve(app, host='0.0.0.0', port=Port) # wun with waitress (production)
