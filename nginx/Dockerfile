FROM nginx:alpine

COPY ./nginx/init-nginx.sh /init-nginx.sh
RUN chmod +x /init-nginx.sh
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx/ssl/localhost.pem /etc/nginx/cert.pem
COPY ./nginx/ssl/localhost-key.pem /etc/nginx/key.pem 

ENTRYPOINT ["/init-nginx.sh"]
