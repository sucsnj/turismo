from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests, os

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv('API_KEY')

def get_coords(city):
    url = f'https://api.geoapify.com/v1/geocode/search?text={city}&apiKey={API_KEY}'
    response = requests.get(url).json()
    if response.get('features'):
        coords = response['features'][0]['geometry']['coordinates']
        lon, lat = coords
        return lat, lon
    return None, None


def get_places(lat, lon):
    url = f'https://api.geoapify.com/v2/places?categories=tourism&filter=circle:{lon},{lat},2000&limit=20&apiKey={API_KEY}'
    response = requests.get(url).json()
    lugares = []
    for f in response.get('features', []):
        prop = f['properties']
        lugar = {
            'nome': prop.get('name', 'Sem nome'),
            'tipo': ','.join(prop.get('categories', [])),
            'lat': f['geometry']['coordinates'][1],
            'lon': f['geometry']['coordinates'][0],
            'place_id': prop.get('place_id'),
            'endereco': prop.get('address_line2', '')
        }
        lugares.append(lugar)
    return lugares


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


@app.route("/health")
def health():
    return "OK", 200


# Se não quiser detalhes extras, pode remover essa rota
@app.route('/detalhes', methods=['GET'])
def detalhes():
    return jsonify({'erro': 'Detalhes não implementados sem Redis'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
