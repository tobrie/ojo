import os.path
import yaml
from string import Template

from . import __appname__, __version__, __configfile__


def relative_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def load_config_dict(filename):
    with open(relative_path(filename)) as f:
        return yaml.safe_load(f)


def new_item_cli():
    item = dict()
    item['name'] = input('name=')
    item['url'] = input('url=')
    item['xpath'] = input('xpath=')
    if not item['xpath']:
        item['xpath'] = None
    item['notify'] = input('notify? [y/N]') == 'y'
    print()

    return item


def get_user_agent():
    return Template(config['requests']['useragent']).substitute(appname=__appname__, version=__version__)


# load app config
#lg.debug('loading app config') # TODO: global debug (lg)
config = load_config_dict(__configfile__)
