from flask import Blueprint, render_template, request, flash, redirect, url_for

from app.database import db

from .forms import RegisterForm, LoginForm
from .models import User


blueprint = Blueprint("user", __name__, url_prefix="/user")


@blueprint.route("/register", methods=["GET", "POST"])
# @login_required
def register():
    form = RegisterForm(request.form)
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
    return render_template("user/register.html", form=form)

@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        # TODO: Login Logic
        flash("You are logged in.", "success")
        return redirect(url_for("index"))
    return render_template("user/login.html", form=form)

@blueprint.route("/logout", methods=["POST"])
def logout():
    pass

