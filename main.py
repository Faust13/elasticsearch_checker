from timeloop import Timeloop
import config as conf
from verification import check_time, check_url
import time
import simplejson as json
import requests
import mail

tl = Timeloop()

@tl.job(interval=conf.PERIOD)
def check_data_4xx_loop():
    errors_4xx = get_metrics(url, time, 400, 499)
    total_count = get_metrics(url, time, 0, 0)
    check_data(errors_4xx, '4xx', total_count)

@tl.job(interval=conf.PERIOD)
def check_data_5xx_loop():
    errors_5xx = get_metrics(url, time, 500, 599)
    total_count = get_metrics(url, time, 0, 0)
    check_data(errors_5xx, '5xx', total_count)

def check_data(err_count, err_code, total_count):
    err_percentage = round(err_count * 100 / total_count, 2)
    if err_percentage < conf.QUALITY_GATE:
        print(f"It's fine! Percentage of errors {err_code} is {err_percentage}%")
    else:
        print(f"Percentage of errors {err_code} is {err_percentage}%! Sending e-mail...")
        alert_type = "firing"
        alert_subject = f"Превышено пороговое значение ошибок {err_code}!"
        alert_text = f"{err_percentage}% обращений ({err_count}/{total_count}) вернули код ошибки {err_code}!"
        mail.sendmail(alert_type, alert_subject, alert_text)
        time.sleep(600)

def get_metrics(url, time, gte, lte):
    if gte == 0 and lte == 0:
        data = {
            "query":{
                    "range":{
                        "@timestamp":{
                            "gt": "now-"+time
                        }
                    }
                }
            }
    else:
        data = {
            "query":{
                "bool":{
                    "must":[
                            {
                            "range":{
                                "code":{
                                    "gte" : gte,
                                    "lte" : lte
                                }
                            }
                        },
                        {
                            "range":{
                                "@timestamp":{
                                    "gt": "now-"+time
                                }
                            }
                        }
                    ]
                }
            }
        }

    r = requests.get(url, data=json.dumps(data), headers=conf.HEADERS)
    result = r.json()
    count = result['count']
    return count


if __name__ == '__main__':
    time = conf.STATS_FOR
    check_time(time)
    url = check_url(conf.ES_HOST, conf.ES_PORT, conf.ES_INDEX)
    tl.start(block=True)