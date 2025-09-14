from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
API_KEY = '5ae2e3f221c38a28845f05b6b17c37432db21ed64fbb106cf2739220'

def get_coords(city):
    url = f'https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={API_KEY}'
    response = requests.get(url).json()
    if 'lat' in response and 'lon' in response:
        return response['lat'], response['lon']
    print(f"Erro ao buscar coordenadas: {response}")
    return None, None

def get_places(lat, lon):
    url = f'https://api.opentripmap.com/0.1/en/places/radius?radius=2000&lon={lon}&lat={lat}&rate=2&format=json&apikey={API_KEY}'
    response = requests.get(url).json()
    return [{'nome': p['name'], 'tipo': p.get('kinds')} for p in response]

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)