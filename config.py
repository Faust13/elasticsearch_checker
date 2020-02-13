import yaml
from datetime import timedelta

with open("config.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

es_host = config['elasticsearch']['host']
es_port = config['elasticsearch']['port']
es_index = config['elasticsearch']['index']
stats_for = config['request']['stats_for']
quality_gate = int(config['rules']['quality_gate'])
period = timedelta(seconds=config['request']['interval'])
email_from = config['email']['from']
email_passwd = config['email']['password']
email_receivers = config['email']['to']


headers = {'Content-type': 'application/json'}