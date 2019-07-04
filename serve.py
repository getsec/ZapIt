import logging
from app import api
from sys import argv
from waitress import serve
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

serve(api, port=argv[1])