# 🌍 Mapa Turístico Interativo

Aplicação web responsiva que permite buscar pontos turísticos em qualquer cidade, visualizar no mapa, acessar imagens (quando disponíveis) e navegar até o local usando Google Maps ou Waze. Utiliza a API [OpenTripMap](https://opentripmap.com/) para fornecer dados turísticos e implementa cache com Redis para otimizar desempenho.

---

## 🚀 Funcionalidades

- 🔎 Busca por endereço ou cidade
- 📍 Exibição de pontos turísticos no mapa via OpenStreetMap
- 🖼️ Popups com nome, tipo e imagem do local (se disponível)
- 🧭 Botões de navegação para Google Maps e Waze
- 📜 Lista interativa com foco automático no mapa
- 🕶️ Interface responsiva para desktop e mobile

---

## 🛠️ Tecnologias Utilizadas

### Frontend
- HTML, CSS, JavaScript
- jQuery para manipulação dinâmica
- Leaflet.js para renderização de mapas interativos

### Backend
- Flask (Python)
- Redis para cache de imagens e dados turísticos

### Integrações
- API pública: [OpenTripMap](https://opentripmap.com/)
- Mapas: OpenStreetMap
- Estilo responsivo com media queries (200px a 1200px)

---

## ⚙️ DevOps e Integração Contínua

Este projeto utiliza **GitHub Actions** para automação de testes e validação de código:

- CI configurada via `main.yml`
- Lint com `flake8` para garantir boas práticas
- Testes automatizados com `pytest`
- Instalação de dependências e ambiente Python 3.13
- Workflow executado automaticamente a cada `push`

> Isso garante qualidade contínua, feedback rápido e segurança nas alterações do código.

---

## 🧠 Sistemas Distribuídos com Redis

Devido às limitações de requisições da API OpenTripMap, o projeto utiliza **Redis** como sistema de cache distribuído:

- Armazena imagens e dados de locais já pesquisados
- Reduz chamadas repetidas à API
- Melhora tempo de resposta e experiência do usuário
- Redis roda como serviço local e pode ser escalado em ambientes distribuídos

---

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/sucsnj/turismo.git
cd turismo

# Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Crie um arquivo .env com sua chave da OpenTripMap
echo API_KEY=coloque_sua_chave_aqui > .env

# Instale o servidor Redis
sudo apt update
sudo apt install redis-server

# Levante o servidor Redis
redis-server --daemonize yes

# Parar Redis
redis-cli shutdown

# Testes e CI
## Para simular um push e ativar o GitHub Actions:

# Cria um commit vazio
git commit --allow-empty -m "Disparar CI"

# Faz o push para o repositório
git push
