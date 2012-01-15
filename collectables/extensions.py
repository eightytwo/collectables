# -*- coding: utf-8 -*-
"""
    extensions.py
    ~~~~~~~~~~~~~~~~~~~~
    
    This module initialises extensions used by the application.

    :copyright: (c) Copyright 2011 by eightytwo.
    :license: BSD, see LICENSE for more details.
"""

from flaskext.sqlalchemy import SQLAlchemy
from flaskext.uploads import IMAGES, UploadSet

db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)
