import configparser
from datetime import timedelta


config = configparser.ConfigParser()
config.read('checker.conf')
es_host = config['ELASTICSEARCH']['host']
es_port = config['ELASTICSEARCH']['port']
es_index = config['ELASTICSEARCH']['index']
stats_for = config['REQUEST']['stats_for']
quality_gate = int(config['RULES']['quality_gate'])
period = timedelta(seconds=int(config['REQUEST']['interval']))

headers = {'Content-type': 'application/json'}