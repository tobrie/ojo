import datetime

from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from .utils import config


class FetchEntry(Base):
    __tablename__ = 'fetch_entries'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.datetime.utcnow)
    item_id = Column(Integer, ForeignKey('items.id'))
    value = Column(String)
    change = Column(Boolean)

    item = relationship('Item', back_populates='entries')

    def __repr__(self):
        return f"<FetchEntry(item='{self.item.name}', value='{self.value}'>"


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    time_added = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    xpath = Column(String)
    notify = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    # TODO: make use of interval
    interval = Column(Integer, default=config['default_interval'])

    entries = relationship('FetchEntry', order_by=FetchEntry.time.desc(), back_populates='item')

    def __repr__(self):
        return f"<Item(name='{self.name}', url='{self.url}', xpath='{self.xpath}'>"
