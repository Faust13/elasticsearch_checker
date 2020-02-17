from timeloop import Timeloop
import config as conf
from verification import check_time, check_url
import time as timer
import simplejson as json
import requests
import mail


if __name__ == '__main__':
    time = conf.STATS_FOR
    check_time(time)
    url = check_url(conf.ES_HOST, conf.ES_PORT, alert.ES_INDEX)
    import rules
    tl.start(block=True)