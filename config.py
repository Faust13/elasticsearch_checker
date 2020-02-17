import yaml
from datetime import timedelta
import sys

with open("./conf/config.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(sys.exc_info())
        raise exc

ES_HOST = config['elasticsearch'].get('host', '127.0.0.1')
ES_PORT = config['elasticsearch'].get('port', '9200')
KIBANA_URL = config['elasticsearch']['kibana_url']
STATS_FOR = config['request']['stats_for']
QUALITY_GATE = int(config['rules'].get('quality_gate', 10))
PERIOD = timedelta(seconds=config['request']['interval'])
EMAIL_FROM = config['email']['from']
EMAIL_PASSWD = config['email']['password']
EMAIL_RECEIVERS = config['email']['to']


HEADERS = {'Content-type': 'application/json'}