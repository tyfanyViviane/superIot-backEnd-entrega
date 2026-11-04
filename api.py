import random
from datetime import datetime, timedelta

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dispositivos com os nomes do seu layout
DISPOSITIVOS = [
    {"id": 1, "nome": "Laboratório 212", "identificador": "irClient-D8BC38A94716"},
    {"id": 2, "nome": "Laboratório A108", "identificador": "sensor-A108"},
    {"id": 3, "nome": "Lab. Info", "identificador": "temp-Lab03"},
    {"id": 4, "nome": "Caixa D'Água", "identificador": "nivel-CX01"},
    {"id": 5, "nome": "Recepção", "identificador": "porta-Entrada"},
]

PROBLEMAS = [
    "Normal",
    "Sinal Wi-Fi fraco",
    "Sem comunicação",
    "Erro no sensor"
]


@app.route('/dispositivos', methods=['GET'])
def listar_dispositivos():
    dados = []

    for dispositivo in DISPOSITIVOS:
        status = random.choice(['online', 'offline', 'desconhecido'])
        horas = random.randint(690, 730)
        data_comunicacao = datetime.now() - timedelta(hours=horas)

        # Formatação do RSSI
        if status == 'online':
            val_rssi = random.randint(-70, -40)
            class_rssi = "Excelente" if val_rssi > -50 else "Bom"
            rssi_str = f"{val_rssi} dBm\n{class_rssi}"
            problema_str = random.choice([PROBLEMAS[0], PROBLEMAS[1]])
        elif status == 'offline':
            val_rssi = random.randint(-90, -80)
            rssi_str = f"{val_rssi} dBm\nPéssimo"
            problema_str = PROBLEMAS[2]
        else:
            rssi_str = "-"
            problema_str = PROBLEMAS[3]

        dados.append({
            'id': dispositivo['id'],
            'dispositivo': f"{dispositivo['nome']}\n{dispositivo['identificador']}",
            'ultima_comunicacao': f"há {horas} h\n{data_comunicacao.strftime('%d/%m/%Y, %H:%M')}",
            'rssi': rssi_str,
            'problema': problema_str,
            'status': status.upper(),
            'contador': 0
        })

    # Retorna o Array diretamente no JSON
    return jsonify(dados)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)