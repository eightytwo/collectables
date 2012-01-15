# -*- coding: utf-8 -*-
"""
    application.py
    ~~~~~~~~~~~~~~~~~~~~
    
    This module runs the application setup.

    :copyright: (c) Copyright 2011 by eightytwo.
    :license: BSD, see LICENSE for more details.
"""

import logging
from logging import Formatter
from logging.handlers import SMTPHandler

from flask import Flask, render_template
from flaskext.uploads import configure_uploads

from collectables.extensions import db, photos
from collectables.utility import session
from collectables import views

__all__ = ["create_app"]

DEFAULT_APP_NAME = "collectables"

DEFAULT_MODULES = (
    (views.frontend, ""),
    (views.account, "/account"),
)

def create_app(config=None, app_name=None, modules=None):
    """Creates and configures the Flask application."""

    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if modules is None:
        modules = DEFAULT_MODULES

    # Create the application object
    app = Flask(app_name)
    
    # Configure the various components of the application
    configure_app(app)
    configure_logging(app)
    configure_extensions(app)
    configure_session(app)
    configure_errorhandlers(app)
    configure_modules(app, modules)
    configure_uploads(app, photos)

    return app

def configure_app(app):
    """Sets up the configuration engine for the application."""
    
    app.config.from_object('collectables.default_settings')
    app.config.from_envvar('COLLECTION_SETTINGS', silent=True)

def configure_modules(app, modules):
    """Registers the modules of the application."""

    for module, url_prefix in modules:
        app.register_module(module, url_prefix=url_prefix)

def configure_logging(app):
    """Sets up the logging engine for the application."""
    
    if app.debug or app.testing:
        return
        
    mail_handler = SMTPHandler(app.config['SMTP_SERVER'],
                               app.config['FROM_ADDRESS'],
                               app.config['ADMINS'],
                               app.config['SUBJECT'])
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(Formatter(
        'Message type:       %(levelname)s'
        'Location:           %(pathname)s:%(lineno)d'
        'Module:             %(module)s'
        'Function:           %(funcName)s'
        'Time:               %(asctime)s'
        ''
        'Message:'
        ''
        '%(message)s'))
    app.logger.addHandler(mail_handler)

def configure_extensions(app):
    """Initialises the database."""
    
    db.init_app(app)

def configure_session(app):
    """Sets up the session management for the application."""
    
    app.session_interface = session.ItsdangerousSessionInterface()

def configure_errorhandlers(app):
    """Sets up the error handlers for the application."""

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('error.html', code=404), 404
