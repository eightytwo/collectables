# -*- coding: utf-8 -*-
"""
    manage.py
    ~~~~~~~~~~~~~~~~~~~~
    
    This module manages the application.

    :copyright: (c) Copyright 2011 by eightytwo.
    :license: BSD, see LICENSE for more details.
"""

from flask import current_app
from flaskext.script import Manager

from collectables import create_app
from collectables.extensions import db

manager = Manager(create_app)

@manager.command
def createall():
    db.create_all()

@manager.command
def dropall():
    db.drop_all()

@manager.shell
def make_shell_context():
    return dict(app=create_app,
                db=db)

if __name__ == '__main__':
    manager.run()
