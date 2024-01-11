#!/bin/sh

# Generate a self-signed SSL certificate
openssl req -x509 -newkey rsa:4096 -keyout /etc/nginx/key.pem -out /etc/nginx/cert.pem -days 365 -nodes -subj '/CN=localhost'

exec nginx -g 'daemon off;'
