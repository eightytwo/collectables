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
from collectables.models.users import User

class Collection(db.Model):
    """Describes a collection which belongs to a user and contains many
    items.
    """

    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(60), nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey(User.id, ondelete='CASCADE'),
                        nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(Collection, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Collection %s>" % self
