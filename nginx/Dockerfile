FROM nginx:alpine

RUN apk --no-cache add curl ca-certificates
RUN curl -L -o /usr/local/bin/mkcert "https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64" \
    && chmod +x /usr/local/bin/mkcert

COPY ./nginx/init-nginx.sh /init-nginx.sh
RUN chmod +x /init-nginx.sh
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

ENTRYPOINT ["/init-nginx.sh"]
