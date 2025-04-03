from flask import render_template
from . import handler_bp
from flask import Flask
from flask_login import current_user


@handler_bp.app_errorhandler(404)
def page_not_found(e):
    print("сработал handler_404")
    return render_template('errors/404.html'), 404

@handler_bp.app_errorhandler(403)
def forbidden(e):
    print(f"сработал handler_403, {current_user}")
    return render_template('errors/403.html'), 403
