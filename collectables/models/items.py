# -*- coding: utf-8 -*-
"""
    items.py
    ~~~~~~~~~~~~~~~~~~~~

    The model that describes an item, belonging to a user's collection.

    :copyright: (c) Copyright 2012 by eightytwo.
    :license: BSD, see LICENCE for details.
"""
from datetime import datetime

from sqlalchemy.dialects.postgresql import ARRAY

from collectables.extensions import db
from collectables.models.collections import Collection

class Item(db.Model):
    """Describes an item which belongs to a user's collection."""

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    safe_id = db.Column(db.String(60), unique=True, nullable=False)
    name = db.Column(db.Unicode(200))
    slug = db.Column(db.Unicode(200))
    description = db.Column(db.UnicodeText)
    collection_id = db.Column(db.Integer,
                              db.ForeignKey(Collection.id, ondelete='CASCADE'),
                              nullable=False)
    photos = db.Column(ARRAY(db.String))
    votes = db.Column(ARRAY(db.Integer))
    tags = db.Column(ARRAY(db.String))
    year = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Item %s>" % self
