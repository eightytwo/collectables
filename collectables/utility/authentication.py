from functools import wraps
from flask import session, request, redirect, url_for

def login_required(f):
    """Decorator function for checking if the user is logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #if 'username' not in session or session['username'] is None:
        if session.get('username') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
