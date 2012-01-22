# -*- coding: utf-8 -*-
"""
    user.py
    ~~~~~~~~~~~~~~~~~~~~
    
    This module contains functions for working with user related views.

    :copyright: (c) Copyright 2012 by eightytwo.
    :license: BSD, see LICENSE for more details.
"""

from flask import current_app, Module, render_template

from collectables.extensions import photos
from collectables.models.users import User

user = Module(__name__)

@user.route("/<username>/")
def collections(username):
    # Get the user who's page is being viewed
    user = User.query.filter_by(username=username).first_or_404()
    
    # Get the statistics of the user's collections
    num_collections, num_items = user.collection_statistics

    # Get a preview of the user's collections
    collections = User.query.collection_preview(user.id)
    
    return render_template("user.html",
                           user=user,
                           num_collections=num_collections,
                           num_items=num_items,
                           collections=collections,
                           photo_base_url=photos.url(""))
