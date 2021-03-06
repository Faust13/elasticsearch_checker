#!/usr/bin/env python3

import yaml
from timeloop import Timeloop
from jinja2 import Environment, FileSystemLoader



if __name__ == '__main__': #generate rules
    config_data = yaml.load(open('./conf/rules.yml'))
    print(config_data)
    env = Environment(loader = FileSystemLoader('./templates'),   trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('rules.py.j2')
    rules_py = template.render(config_data)
    with open("rules.py", "w") as fh:
        fh.write(rules_py)
    import rules