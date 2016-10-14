import logging
import subprocess

class NGINX:
    def __init__(self):
        self._start_nginx()

    def _parse_output(self, process):
        for line in iter(process.stdout.readline, b''):
            log = line.decode("utf-8");
            print(log)

    def _start_nginx(self):
        logging.info("Starting NGINX.")
        cmd = '/usr/sbin/nginx -c /etc/nginx/nginx.conf -t && exec /usr/sbin/nginx -c /etc/nginx/nginx.conf -g "daemon off;"'
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, shell=True)
        self._parse_output(process)
        