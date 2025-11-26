# 🌍 Mapa Turístico Interativo

Aplicação web que permite buscar pontos turísticos em qualquer cidade, visualizar no mapa, acessar imagens (quando disponíveis) e navegar até o local usando Google Maps ou Waze.  
Agora com **cache em Redis** para otimizar buscas e reduzir chamadas à API externa.

---

## 🚀 Funcionalidades

- 🔎 Busca por endereço ou cidade
- 📍 Exibição de pontos turísticos no mapa
- 🧭 Botões de navegação para Google Maps e Waze
- 📜 Lista interativa com foco automático no mapa
- 🕶️ Interface responsiva para desktop e mobile
- ⚡ Cache com Redis para respostas mais rápidas

---

## 🛠️ Tecnologias Utilizadas

- **Frontend**: HTML, CSS, JavaScript, jQuery, Leaflet.js  
- **Backend**: Flask (Python) + Gunicorn  
- **Cache**: Redis  
- **APIs**: [Geoapify](https://www.geoapify.com/)  
- **Mapas**: OpenStreetMap  
- **Estilo responsivo**: Media queries para telas de 200px a 1200px

---

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/sucsnj/turismo.git
cd turismo
```

# Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Crie um arquivo .env com sua chave da Geoapify
echo API_KEY=coloque_sua_chave_aqui > .env

## ⚡ Redis
A aplicação utiliza Redis para armazenar em cache os resultados das buscas de pontos turísticos, evitando chamadas repetidas à API externa e melhorando a performance.

# Usando Docker diretamente
docker run -d --name turismo_redis redis:latest

# Ou via docker-compose (já configurado no projeto)
```
redis:
  image: redis:latest
  container_name: turismo_redis
  restart: always
```

## Subindo o Redis com Docker
# Usando Docker diretamente
docker run -d --name turismo_redis redis:latest

# Ou via docker-compose (já configurado no projeto)
```
redis:
  image: redis:latest
  container_name: turismo_redis
  restart: always
```

## Dependência no backend

Flask>=2.3.0
python-dotenv>=1.0.0
requests>=2.31.0
gunicorn>=21.2.0
redis>=5.0.0

## ▶️ Executando com Docker Compose
```bash
docker compose up --build
```

Frontend disponível em: http://localhost:3000

Backend disponível em: http://localhost:5000

Healthcheck: http://localhost:5000/health

## 📂 Estrutura do Projeto
```
turismo/
├── app.py              # Backend Flask
├── cache.py            # Lógica de cache com Redis
├── requirements.txt    # Dependências Python
├── docker-compose.yml  # Orquestração dos serviços
├── nginx.conf          # Configuração do Nginx
├── templates/
│   └── index.html      # Página principal
└── static/             # CSS, JS e imagens
```

