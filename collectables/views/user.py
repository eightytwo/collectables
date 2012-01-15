# -*- coding: utf-8 -*-
"""
    user.py
    ~~~~~~~~~~~~~~~~~~~~
    
    This module contains functions for working with a user related views.

    :copyright: (c) Copyright 2012 by eightytwo.
    :license: BSD, see LICENSE for more details.
"""

from collectables.models.collections import Collection
from collectables.models.users import User

@user.route("/<username>/")
def collections(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    collections = None

    return render_template("user.html",
                           user=user,
                           num_collections=0,
                           num_items=0,
                           collections=collections)
