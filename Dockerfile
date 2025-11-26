# Imagem base
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copia dependências
COPY requirements.txt .

# Instala dependências (inclui gunicorn para produção)
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia o restante do código
COPY . .

# Expõe a porta do Flask
EXPOSE 5000

# Comando para rodar o app com Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
