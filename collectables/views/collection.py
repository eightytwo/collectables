# -*- coding: utf-8 -*-
"""
    collection.py
    ~~~~~~~~~~~~~~~~~~~~
    
    This module contains functions for working with collection related views.

    :copyright: (c) Copyright 2012 by eightytwo.
    :license: BSD, see LICENSE for more details.
"""

from flask import Module, render_template

#from collectables.models.collections import Collection

collection = Module(__name__)

@collection.route("/<safe_id>/<slug>")
def collection_summary(safe_id):
    collection = Collection.query.filter_by(safe_id=safe_id).first_or_404()
    
    return render_template("collection.html",
                           collection=collection)
