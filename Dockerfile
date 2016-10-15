FROM python:3.5-slim

# Install NGINX, steps retrieved from https://github.com/nginxinc/docker-nginx/blob/master/mainline/jessie/Dockerfile
####
# Copyright (C) 2011-2016 Nginx, Inc.
# All rights reserved.
ENV NGINX_VERSION 1.11.5-1~jessie

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
	&& echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
	&& apt-get update \
	&& apt-get install --no-install-recommends --no-install-suggests -y \
						ca-certificates \
						nginx=${NGINX_VERSION} \
						nginx-module-xslt \
						nginx-module-geoip \
						nginx-module-image-filter \
						nginx-module-perl \
						nginx-module-njs \
						gettext-base \
	&& rm -rf /var/lib/apt/lists/*
####
ENV APP_DIR=/opt/sherpa
WORKDIR $APP_DIR

# Cache requirements packages
COPY ./requirements.txt $APP_DIR
RUN pip install -r requirements.txt

COPY . $APP_DIR

RUN rm -rf /etc/nginx/* && mkdir -p /etc/nginx/conf.d && mkdir -p /etc/sherpa && \
	cp nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 4550

ENTRYPOINT ["./main"]