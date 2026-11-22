FROM alpine/openssl:3.5.9@sha256:9698e7956c08e713265da24c4587205beba3eaa6af2b319d73575d30a6ff033e as ssl
RUN openssl genrsa -out /etc/ssl/private/ssl-cert-snakeoil.key 2048
RUN openssl req -new -key /etc/ssl/private/ssl-cert-snakeoil.key -out /tmp/server.csr -subj "/C=IT/ST=IT/L=Montecarlo/O=Fratres Montecarlo/OU=IT/CN=fratresmontecarlo.org"
RUN openssl x509 -req -days 3650 -in /tmp/server.csr -signkey /etc/ssl/private/ssl-cert-snakeoil.key -out /etc/ssl/certs/ssl-cert-snakeoil.pem

FROM nginx:1.30-alpine@sha256:caf4e1e032a20f9c3c5e28fc7f25ffd768ad8677b4975c54193075997b3a97e3
COPY --from=ssl /etc/ssl/private/ssl-cert-snakeoil.key /etc/ssl/private/ssl-cert-snakeoil.key
COPY --from=ssl /etc/ssl/certs/ssl-cert-snakeoil.pem /etc/ssl/certs/ssl-cert-snakeoil.pem

RUN rm /etc/nginx/conf.d/default.conf
ADD conf.d/* /etc/nginx/conf.d/
