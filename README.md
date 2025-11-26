# 🌍 Mapa Turístico Interativo

Aplicação web que permite buscar pontos turísticos em qualquer cidade, visualizar no mapa, acessar imagens (quando disponíveis) e navegar até o local usando Google Maps ou Waze.

---

## 🚀 Funcionalidades

- 🔎 Busca por endereço ou cidade
- 📍 Exibição de pontos turísticos no mapa
- 🧭 Botões de navegação para Google Maps e Waze
- 📜 Lista interativa com foco automático no mapa
- 🕶️ Interface responsiva para desktop e mobile

---

## 🛠️ Tecnologias Utilizadas

- **Frontend**: HTML, CSS, JavaScript, jQuery, Leaflet.js  
- **Backend**: Flask (Python)  
- **APIs**: [OpenTripMap](https://opentripmap.com/)  
- **Mapas**: OpenStreetMap  
- **Estilo responsivo**: Media queries para telas de 200px a 1200px

---

## 📦 Instalação

```bash
# Clone o repositório
git clone https://https://github.com/sucsnj/turismo.git
cd turismo

# Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Crie um arquivo .env com sua chave da OpenTripMap
echo API_KEY=coloque_sua_chave_aqui > .env


