# -*- coding: utf-8 -*-
"""
    frontend.py
    ~~~~~~~~~~~~~~~~~~~~
    
    This module contains generic view functions which are not specific to a
    model.

    :copyright: (c) Copyright 2012 by eightytwo.
    :license: BSD, see LICENSE for more details.
"""

from flask import Module, render_template

from collectables.models import Item

frontend = Module(__name__)

@frontend.route("/")
def index():
    items = Item.query.order_by('-id')
    return render_template("main.html")

@frontend.route("/search")
def search():
    return render_template("main.html")
