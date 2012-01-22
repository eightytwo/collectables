# -*- coding: utf-8 -*-
"""
    users.py
    ~~~~~~~~~~~~~~~~~~~~

    The model that describes a user of the website.
    
    :copyright: (c) Copyright 2011 by eightytwo.
    :license: BSD, see LICENCE for details.
"""

import hashlib
from datetime import datetime
from itertools import groupby

from flaskext.sqlalchemy import BaseQuery
from sqlalchemy import and_, desc, func, select
from werkzeug import cached_property, generate_password_hash, \
                     check_password_hash

from collectables.extensions import db
from collectables.models.items import Item
from collectables.models.collections import Collection

class UserQuery(BaseQuery):
    """Describes user specific database queries."""

    def authenticate(self, login, password):   
        """Authenticates a user given their login and password."""
        user = self.filter(User.username == login).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    def collection_statistics(self, user_id):
        """Returns the number of collections a user has and the total number
        of items."""
        # Build a subquery to get a list of collections and the item count
        subquery = db.session.query(
            Item.collection_id, func.count(Item.id). \
            label('item_count')). \
            group_by(Item.collection_id).subquery()

        # Filter on the user
        query = db.session.query(
            Collection.id, subquery.c.item_count). \
            filter(and_(Collection.id == subquery.c.collection_id,
                        Collection.user_id == user_id))

        # Execute the query
        summary = query.all()

        return len(summary), sum([c[1] for c in summary])

    def collection_preview(self, user_id):
        """Returns the collections of a user and only the most recent
        items in each collection."""
        # Build a subquery to retrieve items partitioned by collection.
        subquery = select(
            [Item.id, Item.safe_id, Item.name, Item.slug, Item.collection_id,
             Item.photos, func.row_number().over(
                 partition_by=Item.collection_id,
                 order_by=desc(Item.updated)).label('rownumber')]).\
            alias("subquery")

        # Filter the subquery on the user and the rownumber of each
        # partition in order to only retrieve a preview of the items
        # in each of the user's collections. Order by last updated to
        # get the most recent.
        query = db.session.query(
            Collection.id, Collection.safe_id, Collection.name,
            Collection.slug, User.id, User.username, subquery.c.id,
            subquery.c.safe_id, subquery.c.name, subquery.c.slug,
            subquery.c.photos).\
            join(subquery, Collection.id == subquery.c.collection_id).\
            join(User, Collection.user_id == User.id).\
            filter(and_(User.id == user_id,
                        subquery.c.rownumber <= Collection.PREVIEW_SIZE)).\
            order_by(desc(Collection.updated))

        # Execute the query
        preview = query.all()

        # Setup a list to hold the collections, and functions to map out
        # the columns into dictionary items.
        collections = []
        keyfunc = lambda c: {'safe_id': c[1], 'name': c[2], 'slug': c[3]}
        itemfunc = lambda i: {'user_id': i[4], 'username': i[5],
                              'safe_id': i[7], 'name': i[8], 'slug': i[9],
                              'photo': i[10][0]}

        # Group the results by collection and extract the item data.
        for key, group in groupby(preview, keyfunc):
            collection = key
            collection['items'] = map(itemfunc, group)
            collections.append(collection)

        # Return the list of collections.
        return collections

class User(db.Model):
    """Describes a user of the website."""

    __tablename__ = 'users'

    query_class = UserQuery

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(60), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    _password = db.Column("password", db.String(80), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    collections = db.relationship('Collection',
                                  backref='user',
                                  lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.username

    def __repr__(self):
        return "<User %s>" % self

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)  

    password = db.synonym("_password", 
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    @cached_property
    def collection_statistics(self):
        """Returns the number of collections and total number of items of
        this user."""
        try:
            return User.query.collection_statistics(self.id)
        except:
            return 0, 0





    
