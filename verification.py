import re
import simplejson as json
import requests
import config

def check_time(stats_for):
    if not re.match(r"^\d*(m|h|d|w|M|y)$", stats_for):
        raise SystemExit("ERROR: Value of variable 'time' is incorrect: %s" % stats_for)
    
def check_url(es_host, es_port, es_index) -> str:
    url_checker = f"{es_host}:{es_port}/_cluster/health"
    print(url_checker)
    url = f"{es_host}:{es_port}/{es_index}/_count"
    if re.match(r"^(http|https):\/\/[^ ]*$", url):
        r = requests.get(url_checker)
        result = r.json()
        if result['status'] == 'green' or result['status'] == 'yellow':
            return url
        else:
            raise SystemExit("ERROR: Elasticsearch cluster not ready. Cluster status is '%s'" % result['status'])
    else:
        raise SystemExit("ERROR: Value of variable 'url' is incorrect: %s" % url)
