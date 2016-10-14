import os
import logging

def initialize_logger():
    log_level = getattr(logging, os.getenv('LOG_LEVEL', default='WARN').upper(), None)
    logging.basicConfig(level=log_level, format='%(levelname)s:%(name)s:%(asctime)s %(message)s')


            
        