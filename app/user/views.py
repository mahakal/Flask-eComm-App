from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from app.database import db
from app.extensions import bcrypt

from .forms import SignupForm, LoginForm
from .models import User


blueprint = Blueprint("user", __name__, url_prefix="/user")


@blueprint.route("/signup", methods=["GET", "POST"])
# @login_required
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        user = User(
                    username=form.username.data, password=form.password.data,
                    email=form.email.data, dob=form.dob.data, first_name=form.f_name.data, 
                    last_name=form.l_name.data, country_code=form.country_code.data, 
                    mobile_number=form.mobile_number.data ,billing_address=form.billing_address.data,
                    shipping_address=form.shipping_address.data, zip_code=form.zip_code.data,
                    is_active=True, accept_tos=form.accept_tos.data
                )
        db.session.add(user)
        db.session.commit()
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("user.login"))
    return render_template("user/signup.html", form=form)

@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            User.query.filter_by(email=form.username.data).first()
        login_user(user, remeber=True)
        flash("You are logged in.", "success")
        return redirect(url_for("index"))
    return render_template("user/login.html", form=form)

@blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@blueprint.route("/profile", methods=["GET"])
def profile():
    return render_template("user/profile.html")

@blueprint.route("/setting", methods=["GET"])
def setting():
    return render_template("user/setting.html")
