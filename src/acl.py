import logging
import os
import random
import json
import string
import re
from jinja2 import Template

CONST_CONFIG_FILENAME_SIZE = 6

class ACL:
    def __init__(self, mode):    
        with open('/opt/sherpa/config.json', 'r') as conf, open('/opt/sherpa/templates/nginx-acl.tmpl.conf', 'r') as template:
            self._config = json.loads(conf.read())
            self._template = Template(template.read())

        self._allow = True if mode is 'allow' else False
        self._default_allowed_methods = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE']
        self._parse_default()
        self._generate_paths()

    # Creates the default location allowing implicit access
    def _parse_default(self):
        root_config = [x for x in self._config if x['Path'] == '/']
        
        addresses = ['0.0.0.0/0'] if len(root_config) == 0 or 'Addresses' not in root_config[0] else root_config[0]['Addresses']

        default_config = self._template.render(allow=self._allow, path='/', allowed_methods=self._default_allowed_methods, compare='all', addresses=addresses)
        
        # create the default config
        with open('/etc/nginx/conf.d/default.conf', 'w+') as f:
            f.write(default_config)
        

    def _generate_paths(self):
        acls = [config for config in self._config if config['Path'] != '/']
        for acl in acls:
            access = True if acl['Access'] == 'allow' else False
            path = re.sub(r'\*', r'.*', acl['Path'])
            methods = self._default_allowed_methods if 'Methods' not in acl else acl['Methods']
            addresses = ['0.0.0.0/0'] if 'Addresses' not in acl else acl['Addresses']
            
            file_name = '+'.join([acl['Access']] + [acl['Path']] + methods + addresses)
            file_name = '_'.join(re.split('[^+.\w]', file_name))
            
            config = self._template.render(allow=access, path=path, allowed_methods=methods, exact=True, compare=('regex' if '*' in path else 'exact'), addresses=addresses)
            
            # create configs
            with open('/etc/nginx/conf.d/{}.conf'.format(file_name), 'w+') as f:
                f.write(config)


