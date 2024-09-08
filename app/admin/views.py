from flask_admin.contrib.sqla import ModelView
from flask_admin.base import AdminIndexView
from flask_login import current_user, login_required
from flask import url_for, redirect, flash, Blueprint, render_template
from flask_admin import BaseView, expose

from app.models import Order
from app.product.models import Product
from app.user.models import Users
from app.utils import is_admin_required

# Flask-Admin


class AdminModelView(ModelView):
	column_display_pk = True  # optional, but I like to see the IDs in the list

	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_admin


class UserModelView(AdminModelView):
	can_create = False
	can_delete = False
	column_editable_list = ["first_name", "last_name"]
	column_searchable_list = ["username", "email", "mobile_number"]
	column_exclude_list = [
		"_password",
	]
	column_filters = ["created_at"]


class MyAdminIndexView(AdminIndexView):
	@expose("/")
	def index(self):
		if not current_user.is_authenticated:
			flash("Please log in first...", "error")
			return redirect(url_for("user.login"))
		if current_user.is_admin:
			return super(MyAdminIndexView, self).index()
		else:
			return redirect(url_for("index.index"))


class DashboardView(BaseView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_admin

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for("index.index"))

	@expose("/")
	def index(self):
		orders = Order.query.order_by("id").limit(20).all()
		return self.render("_admin/dashboard.html", orders=orders)


# Admin

bp = Blueprint("_admin", __name__, url_prefix="/_admin")


@bp.route("/dashboard", methods=["GET"])
@is_admin_required
@login_required
def dashboard():
	return render_template("_admin/dashboard.html")


@bp.route("/orders", methods=["GET"])
@is_admin_required
@login_required
def orders():
	orders = Order.query.order_by("id").limit(20).all()
	return render_template("_admin/order.html", orders=orders)


@bp.route("/products", methods=["GET"])
@is_admin_required
@login_required
def products():
	products = Product.query.order_by("id").limit(20).all()
	return render_template("_admin/product.html", products=products)


@bp.route("/users", methods=["GET"])
@is_admin_required
@login_required
def users():
	users = Users.query.order_by("id").limit(20).all()
	return render_template("_admin/user.html", users=users)
