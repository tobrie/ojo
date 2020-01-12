import datetime

from PyRSS2Gen import RSS2, RSSItem

from .models import FetchEntry
from .utils import config


def make_items(db):
    for entry in db.query(FetchEntry).filter(FetchEntry.change==True).all():
        rss_item = RSSItem(
                title=entry.item.name + ' has changed',
                link=entry.item.url,
                description=entry.value,
                guid='',
                pubDate=entry.time,
        )
        yield rss_item


def build_feed(db):
    rss = RSS2(
            title='RSS feed',
            link='https://example.com',
            description='changes ...',
            lastBuildDate=datetime.datetime.now(),
            items=make_items(db)
    )

    with open(config['rss']['feedfile'], 'w') as f:
        rss.write_xml(f)
