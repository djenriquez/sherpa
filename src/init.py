import os
import logging
import json

def initialize_logger():
    log_level = getattr(logging, os.getenv('LOG_LEVEL', default='WARN').upper(), None)
    logging.basicConfig(level=log_level, format='%(levelname)s:%(name)s:%(asctime)s %(message)s')

def load_configuration():
    config = []
    # Parse mounted configuration
    for filename in os.listdir('/etc/config/'):
        conf = open('/etc/config/{}'.format(filename), 'r').read()
        config += json.loads(conf)

    # Add env config
    env_config = os.getenv('CONFIG', default=None)
    if env_config is not None:
        config += json.loads(env_config)
    
    # Create main configuration
    f = open('/opt/sherpa/config.json', 'w+')
    f.write(json.dumps(config))
        