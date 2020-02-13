import re
import simplejson as json
import requests
import config

def time():
    if re.match(r"^\d*(m|h|d|w|M|y)$", config.stats_for):
        return config.stats_for
    else:
        raise SystemExit("ERROR: Value of variable 'time' is incorrect: %s" % time)
    
def url():
    url_checker = config.es_host+":"+config.es_port+"/_cluster/health"
    url = config.es_host+":"+config.es_port+"/"+config.es_index+"/_count"
    if re.match(r"^(http|https):\/\/[^ ]*$", url):
        r = requests.get(url_checker, headers=config.headers)
        result = r.json()
        if result['status'] == 'green' or result['status'] == 'yellow':
            return url
        else:
            raise SystemExit("ERROR: Elasticsearch cluster not ready. Cluster status is '%s'" % result['status'])
    else:
        raise SystemExit("ERROR: Value of variable 'url' is incorrect: %s" % url)
