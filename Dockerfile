FROM nginx:1.11.5

RUN rm -rf /etc/nginx/*

ADD src/proxy.conf /etc/nginx/proxy.conf
ADD start.sh /opt/start.sh

EXPOSE 4550

CMD ["/opt/start.sh"]