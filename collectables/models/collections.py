# -*- coding: utf-8 -*-
"""
    collections.py
    ~~~~~~~~~~~~~~~~~~~~

    The model that describes a collection which belongs to a user and contains
    many items.

    :copyright: (c) Copyright 2012 by eightytwo.
    :license: BSD, see LICENCE for details.
"""

from datetime import datetime

from collectables.extensions import db

class Collection(db.Model):
    """Describes a collection which belongs to a user and contains many
    items.
    """

    __tablename__ = 'collections'

    # The number of collections to display on a single page.
    PER_PAGE = 10

    # The number of collections to display on a single page.
    PREVIEW_SIZE = 5
    
    id = db.Column(db.Integer, primary_key=True)
    safe_id = db.Column(db.String(60), unique=True, nullable=False)
    name = db.Column(db.Unicode(60), nullable=False)
    slug = db.Column(db.Unicode(200), nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('Item',
                            backref='collection',
                            lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Collection, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Collection %s>" % self
