from timeloop import Timeloop
import config as conf
from verification import check_time, check_url
import time as timer
import simplejson as json
import requests
import mail

tl = Timeloop()

total_data = {
    "query":{
        "range":{
            "@timestamp":{
                "gt": f"now-{time}"
            }
        }
    }
}


url_5xx = check_url(conf.ES_HOST, conf.ES_PORT, alert['target_index'])
time = conf.STATS_FOR
check_time(time)

@tl.job(interval=conf.PERIOD)
def check_data_5xx_loop():
    data = {"query":{"bool":{"must":[{"range":{"code":{"gte" : 500, "lte" : 599}}},{"range":{"@timestamp":{"gt": "now-"+time}}}]}}}
    errors_5xx = get_count(url, time, data)
    total_count = get_count(url, time, total_data)
    check_count(errors_5xx, 5xx, total_count)


url_4xx = check_url(conf.ES_HOST, conf.ES_PORT, alert['target_index'])
time = conf.STATS_FOR
check_time(time)

@tl.job(interval=conf.PERIOD)
def check_data_4xx_loop():
    data = {"query":{"bool":{"must":[{"range":{"code":{"gte" : 400, "lte" : 599}}},{"range":{"@timestamp":{"gt": "now-"+time}}}]}}}
    errors_4xx = get_count(url, time, data)
    total_count = get_count(url, time, total_data)
    check_count(errors_4xx, 4xx, total_count)


def check_count(err_count, err_code, total_count):
    err_percentage = round(err_count * 100 / total_count, 2)
    if err_percentage < conf.QUALITY_GATE:
        print(f"It's fine! Percentage of errors {err_code} is {err_percentage}%")
    else:
        print(f"Percentage of errors {err_code} is {err_percentage}%! Sending e-mail...")
        alert_type = "firing"
        alert_subject = f"Превышено пороговое значение ошибок {err_code}!"
        alert_text = f"{err_percentage}% обращений ({err_count}/{total_count}) вернули код ошибки {err_code}!"
        mail.sendmail(alert_type, alert_subject, alert_text)
        timer.sleep(600)

def get_count(url, time, data):
    r = requests.get(url, data=json.dumps(data), headers=conf.HEADERS)
    result = r.json()
    count = result['count']
    return count