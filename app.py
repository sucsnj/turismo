from flask import Flask, request, jsonify, render_template
from redis_client import redis_client
from dotenv import load_dotenv
import requests
import os
import json

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv('API_KEY')


def buscar_detalhes_xid(xid):
    cache_key = f"xid:{xid}"
    cached = redis_client.get(cache_key)

    if cached:
        print("Tem cache!")
        return json.loads(cached)
    
    print("Sem cache - procurando na API")
    url = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}?apikey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        detalhes = response.json()
        redis_client.setex(cache_key, 86400, json.dumps(detalhes))
        return detalhes
    else:
        return None


def get_coords(city):
    url = f'https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={API_KEY}'
    response = requests.get(url).json()
    return response.get('lat'), response.get('lon')


def get_places(lat, lon):
    url = f'https://api.opentripmap.com/0.1/en/places/radius?radius=2000& \
        lon={lon}&lat={lat}&rate=2&format=json&apikey={API_KEY}'
    response = requests.get(url).json()
    return [
        {
            'nome': p['name'],
            'tipo': p.get('kinds'),
            'lat': p['point']['lat'],
            'lon': p['point']['lon'],
            'xid': p['xid']
        }
        for p in response
    ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pontos', methods=['GET'])
def pontos_turisticos():
    cidade = request.args.get('endereco')
    if not cidade:
        return jsonify({'erro': 'Endereço não fornecido'}), 400

    lat, lon = get_coords(cidade)
    if not lat or not lon:
        return jsonify({'erro': 'Localização não encontrada'}), 400

    pontos = get_places(lat, lon)
    return jsonify(pontos)

@app.route('/detalhes', methods=['GET'])
def detalhes():
    xid = request.args.get('xid')
    if not xid:
        return jsonify({'erro': 'XID não fornecido'}), 400

    dados = buscar_detalhes_xid(xid)
    if not dados:
        return jsonify({'erro': 'Detalhes não encontrados'}), 404

    return jsonify(dados)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
