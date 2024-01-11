#!/bin/sh

mkcert -install
mkcert -key-file /etc/nginx/key.pem -cert-file /etc/nginx/cert.pem localhost

exec nginx -g 'daemon off;'
