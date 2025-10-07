# Importa os módulos necessários do Flask e outras bibliotecas
from flask import Flask, request, jsonify, render_template
from redis_client import redis_client  # Cliente Redis personalizado para cache
from dotenv import load_dotenv         # Carrega o .env
import requests                        # Para fazer requisições HTTP
import os                              # Para acessar variáveis de ambiente
import json                            # Para manipular dados JSON

# Cria a aplicação Flask
app = Flask(__name__)

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
API_KEY = os.getenv('API_KEY')  # Obtém a chave da API da variável de ambiente

# URL base da API OpenTripMap
base = "https://api.opentripmap.com/0.1/en/places/"


# Função para buscar detalhes de um ponto turístico usando o xid
def buscar_detalhes_xid(xid):
    cache_key = f"xid:{xid}"  # Define a chave de cache
    cached = redis_client.get(cache_key)  # Tenta obter os dados do cache

    if cached:
        print("Tem cache!")  # Log para indicar que os dados vieram do cache
        return json.loads(cached)  # Retorna os dados em formato JSON

    print("Sem cache - procurando na API")
    query = f"xid/{xid}?apikey={API_KEY}"  # Monta a URL da requisição
    url = base + query
    response = requests.get(url)  # Faz a requisição à API

    if response.status_code == 200:
        detalhes = response.json()  # Converte a resposta em JSON
        redis_client.setex(cache_key, 86400, json.dumps(detalhes))  # Cache de 1 dia
        return detalhes
    else:
        return None  # Retorna None se a requisição falhar


# Função para obter latitude e longitude de uma cidade
def get_coords(city):
    query = f'geoname?name={city}&apikey={API_KEY}'
    url = base + query
    response = requests.get(url).json()  # Converte para JSON
    return response.get('lat'), response.get('lon')


# Função para buscar pontos turísticos próximos a uma coordenada
def get_places(lat, lon):  # Parâmetros
    query = f'radius?radius=2000&lon={lon}&lat={lat}&rate=2&format=json&'
    api = f'apikey={API_KEY}'
    url = base + query + api
    response = requests.get(url).json()
    return [
        {
            'nome': p['name'],              # Nome do ponto turístico
            'tipo': p.get('kinds'),         # Tipos ou categorias
            'lat': p['point']['lat'],       # Latitude
            'lon': p['point']['lon'],       # Longitude
            'xid': p['xid']                 # Identificador único
        }
        for p in response  # Itera sobre os resultados
    ]


# Rota principal que renderiza o template HTML
@app.route('/')
def index():
    return render_template('index.html')


# Rota para buscar pontos turísticos com base no endereço fornecido
@app.route('/pontos', methods=['GET'])
def pontos_turisticos():
    cidade = request.args.get('endereco')  # Obtém o endereço da query string
    if not cidade:
        return jsonify({'erro': 'Endereço não fornecido'}), 400

    lat, lon = get_coords(cidade)  # Obtém coordenadas da cidade
    if not lat or not lon:
        return jsonify({'erro': 'Localização não encontrada'}), 400

    pontos = get_places(lat, lon)  # Busca pontos turísticos
    return jsonify(pontos)  # Retorna os pontos em formato JSON


# Rota para buscar detalhes de um ponto turístico específico
@app.route('/detalhes', methods=['GET'])
def detalhes():
    xid = request.args.get('xid')  # Obtém o xid da query string
    if not xid:
        return jsonify({'erro': 'XID não fornecido'}), 400

    dados = buscar_detalhes_xid(xid)  # Busca os detalhes usando o xid
    if not dados:
        return jsonify({'erro': 'Detalhes não encontrados'}), 404

    return jsonify(dados)  # Retorna os detalhes em formato JSON


# Executa a aplicação Flask em modo debug na porta 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)
