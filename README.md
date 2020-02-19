[RUS](https://github.com/Faust13/elasticsearch_checker/blob/master/README.md) | [ENG](https://github.com/faust13/elasticsearch_checker/blob/master/README-EN.md)
# elasticsearch_checker

Всем привет! Это приложение может оказаться полезным для вас, если вы храните логи в Elasticsearch и ищете утилиту, которая могла бы оповещать вас  о том, что что-то пошло не так.

## How to start

Клонируйте этот проект, создайте конфигурационные файлы и запустите `main.py`

## Config

Существует 2 конфигурационных файла:
- `./conf/config.yml` хранит основные настройки, такие какe хост и порт Elasticsearch, значение временного интервала, с которым будет выполняться проверка правил, настройки электронной почты (from, to) etc.
- `./conf/rules.yml` тут описываются сами правила: задаются их имена, условия срабатывания алерта и т.п.

Если вы ранее использовали *Prometheus*, такая структура конфигурационных файлов может показаться знакомой.

См. `./conf/*.examples`.

### config.yml

#### elasticsearch
Эта секция содержит информацию о вашем Elasticsearch:
- `host`: ДОЛЖЕН начинаться с префикса `http://` или `https://` и НЕ ДОЛЖЕН содержать слеша (`/`) В конце. Значение по умолчанию `http://127.0.0.1`
- `port`: Порт вашего Elasticsearch. `9200` по умолчанию
- `kibana_url`: вы можете разместить тут ссылку на ваш дашборд в Kibana. Когда приложение отправляет алерт по электронной почте, письмо содежрит большую кнопку "look in Kibana". По умолчанию `None`

#### request
`request` Содержит информацию о временном интервале для мониторинга
- `stats_for` - за какое количество времени брать информацию из эластика. Формат: `10m`/`5h`/etc. `10m` по умолчанию.
- `interval` - сколько выжидать между обращениями в эластик, в секундах. `5` по умолчанию.


#### email
`email` содержит информацию для оповещений по эл.почте:
- `from`. По умолчанию `elastic_checker@example.com`
- `to`. По умолчанию `example@example.com`

### rules.yml

Файл правил выглядит как-то так:

```yaml
rules:
  - name: '5xx' #имя
    expr: err_percentage > 5 # когда true - отправить алерт
    type: 'count' #Тип метрики. Пока поддеживается только 'count'.
    request: #инфо для запроса
      query: '{"query":{"bool":{"must":[{"range":{"code":{"gte" : 500, "lte" : 599}}},{"range":{"@timestamp":{"gt": "now-"+time}}}]}}}' #query for search
      target_index: 'nginx-access-*' #целевой index в эластике
    silence: 600 #если алерт отправлен - приостановить скраппиг на %silence% секунд

  - alert: '4xx'
    expr: err_percentage > 5
    type: 'count'
    request:
      query: '{"query":{"bool":{"must":[{"range":{"code":{"gte" : 400, "lte" : 599}}},{"range":{"@timestamp":{"gt": "now-"+time}}}]}}}'
      target_index: 'nginx-access-*'
    silence: 600 
```
Чтобы узнать больше о правилах формирования запрса в Elasticsearch через count API, ознакомьтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-count.html)