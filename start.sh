#!/bin/sh
/usr/sbin/nginx -c /etc/nginx/proxy.conf -t && exec /usr/sbin/nginx -c /etc/nginx/proxy.conf -g "daemon off;"