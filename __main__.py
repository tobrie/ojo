import logging
import logging.config
import sys

from . import __appname__, __version__
from .ojo import Ojo
from .models import Item
from .utils import load_config_dict, new_item_cli


# load logging config
log_config = load_config_dict('logging.yaml')
logging.config.dictConfig(log_config)

# start logging
lg = logging.getLogger(__name__)

# load app config
lg.debug('loading app config')

logging.debug(__appname__ + ' ' + __version__)

# start
lg.debug('starting ' + __appname__)
ojo = Ojo()
#ojo.run()


if __name__ == '__main__':
    # TODO: create decent way to add items
    if len(sys.argv) > 1 and sys.argv[1] == 'add':
        itemdict = new_item_cli()
        ojo.db.add(Item(**itemdict))
        ojo.db.commit()

    if input('keep running? [Y/n]') != 'n':
        ojo.run()
    else:
        ojo.check_all()
