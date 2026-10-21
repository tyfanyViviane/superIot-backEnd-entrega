import random
from datetime import datetime, timedelta

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DISPOSITIVOS = [
    {"id": 1, "nome": "Sensor de Temperatura", "localizacao": "Laboratório de Robótica"},
    {"id": 2, "nome": "Controle de Ar-Condicionado", "localizacao": "Sala A-12"},
    {"id": 3, "nome": "Sensor de Umidade", "localizacao": "Biblioteca"},
    {"id": 4, "nome": "Controle de Acesso", "localizacao": "Entrada Principal"},
    {"id": 5, "nome": "Sensor de Nível", "localizacao": "Reservatório de Água"},
]

PROBLEMAS = [
    {"descricao": "Nenhum problema identificado", "gravidade": 0},
    {"descricao": "Sinal Wi-Fi fraco", "gravidade": 1},
    {"descricao": "Comunicação instável", "gravidade": 2},
    {"descricao": "Dispositivo sem comunicação", "gravidade": 3},
]


@app.route('/dispositivos', methods=['GET'])
def listar_dispositivos():
    dados = []

    for dispositivo in DISPOSITIVOS:
        status = random.choice(['online', 'offline', 'desconhecido'])
        ultima_comunicacao = datetime.now() - timedelta(minutes=random.randint(0, 180))
        rssi = random.randint(-95, -35) if status == 'online' else None

        if status == 'online':
            problema = random.choice(PROBLEMAS[:3])
        elif status == 'offline':
            problema = PROBLEMAS[3]
        else:
            problema = {"descricao": "Estado do dispositivo desconhecido", "gravidade": 2}

        dados.append({
            'id': dispositivo['id'],
            'status': status,
            'dispositivo': {
                'nome': dispositivo['nome'],
                'localizacao': dispositivo['localizacao'],
            },
            'ultima_comunicacao': ultima_comunicacao.isoformat(timespec='seconds'),
            'rssi': rssi,
            'problema': problema,
        })

    return jsonify({'dados': dados})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)