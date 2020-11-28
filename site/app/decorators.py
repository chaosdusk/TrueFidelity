from functools import wraps

from flask import g, request, redirect, url_for, flash
from app import constants
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Must be admin to access this page', 'warning')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def active_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or (current_user.status == constants.INACTIVE and not current_user.is_admin):
            flash('Must have activated account to access this page', 'warning')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function