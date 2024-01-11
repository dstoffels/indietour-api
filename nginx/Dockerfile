FROM nginx:alpine
COPY ./init-nginx.sh /init-nginx.sh
RUN chmod +x /init-nginx.sh
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
ENTRYPOINT ["/init-nginx.sh"]
