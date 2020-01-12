import logging
import time
from io import StringIO
from urllib.parse import urlparse

import requests
from lxml import etree
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .telegram import Telegram
from . import Base, __appname__, __version__
from .models import FetchEntry, Item
from .utils import relative_path, config, get_user_agent


class Ojo:
    def __init__(self):
        # TODO: make logger (lg) global
        self.lg = logging.getLogger(__name__)

        self.session = requests.Session()
        self.session.headers = {'User-Agent': get_user_agent()}
        self.interval = config['fetch_interval']

        db_engine = create_engine('sqlite:///' + relative_path(config['dbfile']))
        Base.metadata.create_all(db_engine)
        DBSession = sessionmaker(bind=db_engine)
        self.db = DBSession()

        self.telegram = Telegram()

        # output number of items
        items = self.db.query(Item)
        items_active = items.filter(Item.active)
        self.lg.info(f'found {len(items_active.all())} active items ({len(items.all())} total)')

    def fetch_item(self, item):
        # make request
        self.lg.debug(f'GET {item.url}')
        response = self.session.get(item.url)
        self.lg.debug(f'got response, status: {response.status_code}')
        result = response.text

        # TODO: check if it works with broken html
        if item.xpath:
            tree = etree.parse(StringIO(response.text), parser=etree.HTMLParser())
            result = tree.xpath(item.xpath)
        # TODO: css selector support (https://lxml.de/cssselect.html)

        # take only first element
        # TODO: other return types, see https://lxml.de/xpathxslt.html
        if isinstance(result, list):
            if len(result) == 0:
                self.lg.warning('empty result')
                return None
            elif len(result) > 1:
                # raise Exception('unspecific xpath: more than one result')
                self.lg.warning('unspecific xpath: more than one result')

            result = result[0]

        return result

    def check_all(self):
        self.lg.info('checking all items for changes')
        items = self.db.query(Item).all()

        for i, item in enumerate(items):
            netloc = urlparse(item.url).netloc
            self.lg.info(f'checking {netloc} ({i+1}/{len(items)})')

            # TODO: proper handling of return values
            res = self.fetch_item(item)
            if isinstance(res, etree._Element):
                res = res.text

            print(res)

            if len(item.entries) > 0:
                most_recent = item.entries[0]

                # detect changes
                if res != most_recent.value:
                    self.lg.info('detected change')
                    if item.notify:
                        self.lg.info('sending notification')
                        text = f"There has been a change for item '{item.name}', see {item.url}"
                        self.telegram.notify(text)
                else:
                    self.lg.info('no change')

            entry = FetchEntry(item=item, value=res)
            self.db.add(entry)
            self.db.commit()

    def run(self):
        self.lg.info(f'running with {self.interval}s interval')
        while True:
            self.check_all()
            time.sleep(self.interval)
