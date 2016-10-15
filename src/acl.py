import logging
import os
import random
import json
import string
import re
from jinja2 import Template

class ACL:
    def __init__(self, mode):
        self._config = json.loads(open('/opt/sherpa/config.json', 'r').read())
        self._allow = True if mode is 'allow' else False
        self._template = Template(open('/opt/sherpa/templates/nginx-acl.tmpl.conf', 'r').read())
        self._default_allowed_methods = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE']
        self._parse_mode()
        self._generate_paths()

    # Creates the default location allowing implicit access
    def _parse_mode(self):
        default_config = self._template.render(allow=self._allow, path='/', allowed_methods=self._default_allowed_methods, compare='all')
        # create the default config
        f = open('/etc/nginx/conf.d/default.conf', 'w+')
        f.write(default_config)
        

    def _generate_paths(self):
        for acl in self._config:
            access = True if acl['Access'] == 'allow' else False
            path = re.sub(r'\*', r'.*', acl['Path'])
            compare = 'regex' if '*' in path else 'exact'
            methods = self._default_allowed_methods if 'Methods' not in acl else acl['Methods']
            
            random_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

            config = self._template.render(allow=access, path=path, allowed_methods=methods, exact=True, compare=compare)
            
            # create configs
            f = open('/etc/nginx/conf.d/{}.conf'.format(random_name), 'w+')
            f.write(config)


