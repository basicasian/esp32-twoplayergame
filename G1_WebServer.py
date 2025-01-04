from flask import Flask, request, jsonify
import random
import sys

app = Flask(__name__)

round = 1
max_rounds = 6
clients_connected = 0
max_clients = 2
round_leds = []
round_generated = False
round_log = []
round_clients_finished = []

@app.route('/ready', methods=['POST'])
def client_ready():
    global clients_connected
    clients_connected += 1
    data = { 
        'message' : 'OK', 
        'clientnumber' : clients_connected - 1, 
    } 
    return jsonify(data) 

@app.route('/start', methods=['GET'])
def all_clients_ready():
    global round_log, clients_connected, max_clients
    if clients_connected == max_clients:
        round_log = [0 for _ in range(max_clients)]
        return jsonify({ 'message' : 'OK', 'rounds': max_rounds })
    else:
        return jsonify({ 'message' : 'NOT OK' })

@app.route('/round_start', methods=['POST'])
def start_round():
    global round_clients_finished
    if all(round_clients_finished):
        round_clients_finished = [False for _ in range(max_clients)]
    return jsonify({ 'message' : 'OK' })

@app.route('/round', methods=['GET'])
def generate_round():
    global round_leds, round, round_generated, round_clients_finished
    if round_generated == False:
        round_leds = [random.randint(0, 3) for _ in range(round + 1)]
        round_generated = True
    return jsonify({ 'message': 'OK','round' : round, 'leds' : round_leds })

@app.route('/round_finished', methods=['POST'])
def finished_round():
    global round_log, round_leds, round_generated, round, max_rounds, round_clients_finished
    data = request.json
        
    round_clients_finished[data.get('player')] = True

    if not all(round_clients_finished):
        return jsonify({ 'message' : 'WAIT'})        

    if round_generated == True:
        round_generated = False
        round += 1

    if round > max_rounds:
        if round_leds == data.get('leds'):
            round_log[data.get('player')] += round - 1
        return jsonify({ 'message' : 'FINISH'})

    if round_leds == data.get('leds'):
        round_log[data.get('player')] += round - 1
        return jsonify({ 'message' : 'OK' })
    else:
        return jsonify({ 'message' : 'NOT OK' })

@app.route('/score', methods=['GET'])
def get_score():
    global round_log
    return jsonify({ 'message' : 'OK', 'score' : round_log })

@app.route('/my_place', methods=['GET'])
def get_my_place():
    global round_log
    player = request.args.get('player')
    ranking = sum(x > round_log[int(player)] for x in round_log) + 1
    return jsonify({ 'message' : 'OK', 'place' : ranking })

if __name__ == '__main__':
    app.run(host='0.0.0.0')

