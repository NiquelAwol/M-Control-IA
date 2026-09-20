FROM nginx:alpine

# Copiar archivos estaticos del proyecto al directorio publico de Nginx
COPY ./Proyecto /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
