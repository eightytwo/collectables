# -*- coding: utf-8 -*-
"""
    account.py
    ~~~~~~~~~~~~~~~~~~~~
    
    This module contains view functions for working with a user's account.

    :copyright: (c) Copyright 2012 by eightytwo.
    :license: BSD, see LICENSE for more details.
"""

from flask import flash, Module, render_template, redirect, request, session, \
                  url_for

from collectables.extensions import db
from collectables.forms import LoginForm, RegisterForm
from collectables.models import Item, User

account = Module(__name__)

@account.route("/login/", methods=("GET", "POST"))
def login():  
    form = LoginForm(login=request.args.get("username", None),
                     next=request.args.get("next", None))

    if form.validate_on_submit():
        user, authenticated = User.query.authenticate(form.username.data,
                                                      form.password.data)

        if user and authenticated:
            # Setup the session
            session['logged_in'] = True
            session['username'] = user.username

            # Send the user to a redirect URL if present or their main page
            next_url = form.next.data
            if not next_url or next_url == request.path:
                next_url = url_for('user.collections', username=user.username)

            return redirect(next_url)
        else:
           flash("Sorry, you were unable to be authenticated.", 'error')

    return render_template("login.html", form=form)

@account.route("/logout/")
def logout():
    # Clear the session
    session.pop('logged_in', None)
    session.pop('username', None)

    # Setup the flash to notify the user
    flash("You have been logged out. Happy collecting :)", 'info')
    
    # Redirect to the main page
    return redirect(url_for('frontend.index'))

@account.route("/register/", methods=("GET", "POST"))
def register():
    form = RegisterForm(next=request.args.get("next"))

    if form.validate_on_submit():
        # Construct and populate a new user object
        user = User()
        form.populate_obj(user)

        # Add the user to the database
        db.session.add(user)
        db.session.commit()

        # Setup the session
        session['logged_in'] = True
        session['username'] = user.username
        
        # Welcome the user via the flash
        flash("Welcome to Collections!", 'info')

        # Send the user to a redirect URL if present or their main page
        next_url = form.next.data
        if not next_url or next_url == request.path:
            next_url = url_for('user.collections', username=user.username)

        return redirect(next_url)
    
    return render_template("register.html", form=form)
