# -*- coding: utf-8 -*-
"""
    default_settings.py
    ~~~~~~~~~~~~~~~~~~~~
    
    This module contains the default application settings.
    
    Environment specific/sensitive settings are contained within a separate
    configuration file accessibly by a PATH variable present on each particular
    environment.

    :copyright: (c) Copyright 2011 by eightytwo.
    :license: BSD, see LICENSE for more details.
"""

# Application execution settings
DEBUG = True 
TESTING = False

# Database settings
SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@localhost:5433/collectables'

# Logging settings
ADMINS = ['eightytwo']
SMTP_SERVER = '127.0.0.1'
FROM_ADDRESS = 'user@host.net'
SUBJECT = 'Application Failure'

# Session secret key
SECRET_KEY = '\x83\xa5\xa4\xf7\xa9\xe5=\xfd\xc0\xb8\x1f\xab\x8b\x10\\z\xb3\x81\x1a\x9f\xffo7\xf7'

# Upload directory
UPLOADED_PHOTOS_DEST = '/tmp/collectables/photos'

# General application settings
ITEMS_PER_PAGE = 2
