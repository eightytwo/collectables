# -*- coding: utf-8 -*-
"""
    account.py
    ~~~~~~~~~~~~~~~~~~~~
    
    This module contains forms for working with a user's account.

    :copyright: (c) Copyright 2012 by eightytwo.
    :license: BSD, see LICENSE for more details.
"""

from urlparse import urlparse, urljoin

from flask import request, url_for
from flaskext.wtf import Form, HiddenField, TextField, PasswordField, \
                         FileField, TextAreaField, Email, \
                         ValidationError, Required, Length, EqualTo, regexp

from collectables.models.users import User

REQUIRED_MSG = "%s is a mandatory field."
USERNAME_RE = r'^[\w.+-]+$'

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

class RedirectForm(Form):
    """Form with handling for safe url redirection."""
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='main', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))

class LoginForm(RedirectForm):
    """Describes the form fields and validation for the login form."""
    username = TextField('username', [Required(REQUIRED_MSG % "Username")]) 
    password = PasswordField('password', [Required(REQUIRED_MSG % "Password")])

class RegisterForm(RedirectForm):
    """Describes the form fields and validation for the register form."""
    username = TextField(
        'username',
        [Required(REQUIRED_MSG % "Username"),
         regexp(USERNAME_RE,
                message=("You can only use letters, numbers or dashes"))])
    email = TextField('email',
                      [Required(REQUIRED_MSG % "Email"),
                       Email("A valid email address is required.")])
    password = PasswordField('password')
    password_confirm = PasswordField(
        'repeat password',
        [Required(REQUIRED_MSG % "Password"),
         Length(min=6, message="Password must be at least six characters."),
         EqualTo('password', message="Passwords must match.")])

    def validate_username(self, field):
        """Applies additional validation to the username field."""
        user = User.query.filter(User.username.like(field.data)).first()
        if user:
            raise ValidationError("Sorry, that username is already in use.")
        

    def validate_email(self, field):
        """Applies additional validation to the email field."""
        user = User.query.filter(User.email.like(field.data)).first()
        if user:
            raise ValidationError("Sorry, that email is already registered.")
