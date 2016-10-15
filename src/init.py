import os
import logging
import json

def initialize_logger():
    log_level = getattr(logging, os.getenv('LOG_LEVEL', default='WARN').upper(), None)
    logging.basicConfig(level=log_level, format='%(levelname)s:%(name)s:%(asctime)s %(message)s')

def load_configuration():
    config = []
    # Parse mounted configuration
    for filename in os.listdir('/etc/sherpa/'):
        with open('/etc/sherpa/{}'.format(filename), 'r') as conf:
            config += json.loads(conf.read())

    # Add env config
    env_config = os.getenv('CONFIG', default=None)
    if env_config is not None:
        config += json.loads(env_config)
    
    # Create main configuration
    with open('/opt/sherpa/config.json', 'w+') as f:
        f.write(json.dumps(config))
        