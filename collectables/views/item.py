# -*- coding: utf-8 -*-
"""
    item.py
    ~~~~~~~~~~~~~~~~~~~~
    
    This module contains functions for working with item related views.

    :copyright: (c) Copyright 2012 by eightytwo.
    :license: BSD, see LICENSE for more details.
"""

from flask import Module, render_template, session

from collectables.extensions import photos
from collectables.models.items import Item
from collectables.models.users import User

item = Module(__name__)

@item.route("/<safe_id>/<slug>/")
def item_summary(safe_id, slug):
    # Get the item and the id of the owner
    item = Item.query.filter_by(safe_id=safe_id).first_or_404()
    
    # Get the user who owns this item and their statistics
    user = User.query.get_or_404(item.collection.user_id)
    num_collections, num_items = user.collection_statistics

    # Setup flags to for controlling conditional elements on the ui
    logged_in = session.get('logged_in')
    is_owner = (user.username == session.get('username'))
    has_voted = False

    return render_template("item.html",
                           user=user,
                           num_collections=num_collections,
                           num_items=num_items,
                           item=item,
                           logged_in=logged_in,
                           is_owner=is_owner,
                           has_voted=has_voted,
                           photo_base_url=photos.url(""))
