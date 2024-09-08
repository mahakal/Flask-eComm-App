from flask import (
	Blueprint,
	flash,
	redirect,
	render_template,
	request,
	url_for,
	session,
)
from flask_login import login_required, login_user, logout_user

from app.database import db

from .forms import LoginForm, SignupForm
from .models import Address, Users

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/signup", methods=["GET", "POST"])
def signup():
	form = SignupForm(request.form)
	if form.validate_on_submit():
		address = Address(
			billing_address=form.billing_address.data,
			shipping_address=form.shipping_address.data,
			zip_code=form.zip_code.data,
		)
		user = Users(
			username=form.username.data,
			password=form.password.data,
			email=form.email.data,
			dob=form.dob.data,
			first_name=form.f_name.data,
			last_name=form.l_name.data,
			country_code=form.country_code.data,
			mobile_number=form.mobile_number.data,
			addresses=[address],
			is_active=True,
			accept_tos=form.accept_tos.data,
		)
		db.session.add(user)
		db.session.commit()
		flash("Thank you for registering. You can now log in.", "success")
		return redirect(url_for("user.login"))
	return render_template("user/signup.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm(request.form)
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if not user:
			user = Users.query.filter_by(email=form.username.data).first()
		login_user(user, remember=True)
		flash("You are logged in.", "success")
		session["cart_products"] = len(user.cart_products)
		return redirect(url_for("index.index"))
	return render_template("user/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
	logout_user()
	flash("You are logged out", "success")
	return redirect(url_for("index.index"))


@bp.route("/profile", methods=["GET"])
@login_required
def profile():
	return render_template("user/profile.html")
