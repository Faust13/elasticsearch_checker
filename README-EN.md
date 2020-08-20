[RUS](https://github.com/Faust13/elasticsearch_checker/blob/master/README.md) | [ENG](https://github.com/faust13/elasticsearch_checker/blob/master/README-EN.md)
# elasticsearch_checker

Hi there! This app can helps you if you are storring logs in Elasticsearch and looking for notification tool for it.

## How to start

Just clone this repo, create config file & run `main.py`

## Config

There is two configuration files:
- `./conf/config.yml` stores global configuration, like a elasticsearch host & port, refresh interval for checking rules, email settings (from, to) etc.
- `./conf/rules.yml` contains alerts names, expressions, target index etc.

if you have previously used *Prometheus* this can looks similar.

Look to `./conf/*.examples` files to know more.

### config.yml

#### elasticsearch
`elasticsearch` section contains basic info about your Elasticsearch:
- `host`: MUST starts with `http://` or `https://` prefix and do not contain slash (`/`) in the end. Default value is `http://127.0.0.1`
- `port`: just port of your elasticsearch. Default is `9200`
- `kibana_url`: you can place here url to your Kibana dashboard. When app sends e-mail, it contain a big button "look in Kibana". Default is `None`

#### request
`request` contains info about time interval and refresh time
- `stats_for` - time interval for monitoring. Like a kibana time interval format: `10m`/`5h`/etc. Default is `10m`.
- `interval` - scrape interval in seconds. Default is `5` seconds.


#### email
`email` contains info for email notification:
- `from`. Default is `elastic_checker@example.com`
- `to`. Default is `example@example.com`

### rules.yml

Rules file looks like:

```yaml
rules:
  - name: '5xx' #alert name
    expr: err_percentage > 5 # when expression is true application will send alert.
    type: 'count' #type of metric. Only 'count' and 'top_hit' supported now.
    request: #info for request
      query: '{"query":{"bool":{"must":[{"range":{"code":{"gte" : 500, "lte" : 599}}},{"range":{"@timestamp":{"gt": "now-"+time}}}]}}}' #query for search
      target_index: 'nginx-access-*' #target index name
    silence: 600 #if alert was sent - sleep for %silence% seconds

  - alert: '4xx'
    expr: err_percentage > 5
    type: 'count' #type of metric. Only 'count' supported now.
    request:
      query: '{"query":{"bool":{"must":[{"range":{"code":{"gte" : 400, "lte" : 499}}},{"range":{"@timestamp":{"gt": "now-"+time}}}]}}}'
      target_index: 'nginx-access-*'
    silence: 600 
```
This tool can looks only for counts. To learn about Elasticsearch's count API please, read the [documetation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-count.html)
