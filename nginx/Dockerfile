FROM alpine/openssl:latest as ssl
RUN openssl genrsa -out /etc/ssl/private/ssl-cert-snakeoil.key 2048
RUN openssl req -new -key /etc/ssl/private/ssl-cert-snakeoil.key -out /tmp/server.csr -subj "/C=IT/ST=IT/L=Montecarlo/O=Fratres Montecarlo/OU=IT/CN=fratresmontecarlo.org"
RUN openssl x509 -req -days 3650 -in /tmp/server.csr -signkey /etc/ssl/private/ssl-cert-snakeoil.key -out /etc/ssl/certs/ssl-cert-snakeoil.pem

FROM nginx:1.27-alpine
COPY --from=ssl /etc/ssl/private/ssl-cert-snakeoil.key /etc/ssl/private/ssl-cert-snakeoil.key
COPY --from=ssl /etc/ssl/certs/ssl-cert-snakeoil.pem /etc/ssl/certs/ssl-cert-snakeoil.pem

RUN rm /etc/nginx/conf.d/default.conf
ADD conf.d/* /etc/nginx/conf.d/
