from timeloop import Timeloop
import config as conf
import verification as check
import simplejson as json
import requests
import mail

tl = Timeloop()



@tl.job(interval=conf.period)
def check_data_loop():
    errors_4xx = get_metrics(url, time, 400, 499)
    errors_5xx = get_metrics(url, time, 500, 599)
    total_count = get_metrics(url, time, 0, 0)

    err_4xx_percentage = round(errors_4xx * 100 / total_count, 2)
    err_5xx_percentage = round(errors_5xx * 100 / total_count, 2)

    if err_4xx_percentage < conf.quality_gate:
        print("It's fine! Client errors is " +str(err_4xx_percentage)+ "%")
    else:
        if err_4xx_percentage > conf.quality_gate:
            print("Client errors is " +str( err_4xx_percentage)+ "%! Sending e-mail...")
            alert_type = "firing"
            alert_subject = "Превышено пороговое значение ошибок 4xx!"
            alert_text = str(err_4xx_percentage)+"% обращений ("+str(errors_4xx)+"/"+str(total_count)+") вернули код ошибки 4xx!"
            mail.sendmail(alert_type, alert_subject, alert_text)

    if err_5xx_percentage < conf.quality_gate:
        print("It's fine! Server errors is " +str(err_5xx_percentage)+ "%")
    else:
        print("Server errors is " +str(err_5xx_percentage)+ "%! Sending e-mail...")
        alert_type = "firing"
        alert_subject = "Превышено пороговое значение ошибок 5xx!"
        alert_text = str(err_4xx_percentage)+"% обращений ("+str(errors_4xx)+"/"+str(total_count)+") вернули код ошибки 5xx!"
        mail.sendmail(alert_type, alert_subject, alert_text)

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
                "bool": {
                    "must":[
                            {
                            "range" : {
                                "code" : {
                                    "gte" : gte,
                                    "lte" : lte
                                }
                            }
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "gt": "now-"+time
                                }
                            }
                        }
                    ]
                }
            }
        }

    r = requests.get(url, data=json.dumps(data), headers=conf.headers)
    result = r.json()
    count = result['count']
    return count


if __name__ == '__main__':
    time = check.time()
    url = check.url()
    tl.start(block=True)