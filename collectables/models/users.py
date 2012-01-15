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

from flaskext.sqlalchemy import BaseQuery
from werkzeug import generate_password_hash, check_password_hash

from collectables.extensions import db

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

    def collection_summary(self, user_id):
        """Retrieves a summary of a user's collections detailing the number
        of collections they have and the total number of items in all
        collections.
        """
        user = self.get(user_id)

        return user 

class User(db.Model):
    """Describes a user of the website."""

    __tablename__ = 'users'

    query_class = UserQuery

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(60), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    _password = db.Column("password", db.String(80))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)
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
