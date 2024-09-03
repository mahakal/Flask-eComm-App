from flask_login import current_user
from flask import request, redirect, url_for
from functools import wraps
from flask_login.config import EXEMPT_METHODS


def is_admin_required(func):
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if request.method in EXEMPT_METHODS:
			return func(*args, **kwargs)
		elif not current_user.is_admin:
			return redirect(url_for("index.index"))
		return func(*args, **kwargs)

	return decorated_view
