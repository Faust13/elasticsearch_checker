import requests
import simplejson as json
from timeloop import Timeloop
import re
from datetime import timedelta
import configparser

config = configparser.ConfigParser()
headers = {'Content-type': 'application/json'}
config.read('example.ini')
es_host = config['ELASTICSEARCH']['host']
es_port = config['ELASTICSEARCH']['port']
es_index = config['ELASTICSEARCH']['index']
stats_for = config['REQUEST']['stats_for']
quality_gate = int(config['RULES']['quality_gate'])
period = timedelta(seconds=int(config['REQUEST']['interval']))

tl = Timeloop()



@tl.job(interval=period)
def check_data_loop():
    errors_4xx = get_metrics(url, time, 400, 499)
    errors_5xx = get_metrics(url, time, 500, 599)
    total_count = get_metrics(url, time, 0, 0)

    err_4xx_percentage = round(errors_4xx * 100 / total_count, 2)
    err_5xx_percentage = round(errors_5xx * 100 / total_count, 2)

    if err_4xx_percentage < quality_gate:
        print("It's fine! Client errors is " +str(err_4xx_percentage)+ "%")
    else:
        if err_4xx_percentage > quality_gate:
            print("Client errors is " +str( err_4xx_percentage)+ "%! Sending e-mail...")

    if err_5xx_percentage < quality_gate:
        print("It's fine! Server errors is " +str(err_5xx_percentage)+ "%")
    else:
        print("Server errors is " +str(err_5xx_percentage)+ "%! Sending e-mail...")


def check_time():
    if re.match(r"^\d*(m|h|d|w|M|y)$", stats_for):
        return stats_for
    else:
        raise SystemExit("ERROR: Value of variable 'time' is incorrect: %s" % time)
    
def check_url():
    url_checker = es_host+":"+es_port+"/_cluster/health"
    url = es_host+":"+es_port+"/"+es_index+"/_count"
    if re.match(r"^(http|https):\/\/[^ ]*$", url):
        r = requests.get(url_checker, headers=headers)
        result = r.json()
        if result['status'] == 'green' or result['status'] == 'yellow':
            return url
        else:
            raise SystemExit("ERROR: Elasticsearch cluster not ready. Cluster status is '%s'" % result['status'])
    else:
        raise SystemExit("ERROR: Value of variable 'url' is incorrect: %s" % url)

def get_metrics(url, time, gte, lte):
    if gte == 0 and lte == 0:
        data = {"query":{"range": {"@timestamp": {"gt": "now-"+time}}}}
    else:
        data = {"query":{"bool": {"must":[{"range" : {"code" : {"gte" : gte,"lte" : lte}}},{"range": {"@timestamp": {"gt": "now-"+time}}}]}}}

    r = requests.get(url, data=json.dumps(data), headers=headers)
    result = r.json()
    count = result['count']
    return count


if __name__ == '__main__':
    time = check_time()
    url = check_url()
    tl.start(block=True)