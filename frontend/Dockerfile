FROM nginx:latest

# Remove config padrão
RUN rm /etc/nginx/conf.d/default.conf

# Copia nossa config customizada
COPY default.conf /etc/nginx/conf.d/

# Copia arquivos estáticos e templates
COPY ../static /usr/share/nginx/html/static
COPY ../templates /usr/share/nginx/html/templates
