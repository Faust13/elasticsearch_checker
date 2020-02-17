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
KIBANA_URL = config['elasticsearch'].get('kibana_url', None)
STATS_FOR = config['request'].get('stats_for', "10m")
PERIOD = timedelta(seconds=config['request'].get('interval', 5))
EMAIL_FROM = config['email'].get('from', "elastic_checker@example.com")
EMAIL_RECEIVERS = config['email'].get('to', "example@example.com")

HEADERS = {'Content-type': 'application/json'}