import re
from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
	BooleanField,
	DateField,
	IntegerField,
	PasswordField,
	StringField,
)
from wtforms.validators import (
	DataRequired,
	Email,
	EqualTo,
	Length,
	NumberRange,
	ValidationError,
)

from .models import User

username_regex = re.compile(r"\W")


def dob_range(min_age=18, max_age=120):
	message = f"User must be above {min_age} years and under {max_age} years"

	def _range(form, field):
		input_date = field.data
		today_date = date.today()
		min_d = today_date.replace(year=today_date.year - min_age)
		max_d = today_date.replace(year=today_date.year - max_age)
		if not max_d < input_date <= min_d:
			raise ValidationError(message)

	return _range


def email_or_username():
	message = "Please enter a valid username or email"

	def _e_or_u(form, field):
		input_data = field.data
		# TODO: Better Validation for Email
		if username_regex.search(input_data) and (
			"@" not in input_data or "." not in input_data
		):
			raise ValidationError(message)

	return _e_or_u


def valid_username():
	message = "Username should consist of A-z, a-z, 0-9 and _"

	def _u(form, field):
		input_data = field.data

		if username_regex.search(input_data):
			raise ValidationError(message)

	return _u


class SignupForm(FlaskForm):
	f_name = StringField(
		"First Name",
		validators=[DataRequired(), Length(min=3, max=25)],
	)
	l_name = StringField(
		"Last name",
		validators=[DataRequired(), Length(min=3, max=25)],
	)
	dob = DateField(
		"Date of Birth",
		validators=[DataRequired(), dob_range()],
	)
	# TODO: username should consist of Uppercase, LowerCase, Digits, _
	username = StringField(
		"Username",
		validators=[DataRequired(), Length(min=3, max=25), valid_username()],
	)
	email = StringField(
		"Email",
		validators=[DataRequired(), Email(), Length(min=6, max=80)],
	)
	# TODO: country code and validation
	country_code = StringField(
		"Country Code",
		validators=[DataRequired(), Length(min=1, max=6)],
	)
	# TODO: validation
	mobile_number = IntegerField(
		"Mobile Number",
		validators=[DataRequired()],
	)
	# TODO: add rules for password
	# (Upper case, Lower Case, Digit, Special Character)
	password = PasswordField(
		"Password",
		validators=[DataRequired(), Length(min=8, max=40)],
	)
	confirm = PasswordField(
		"Verify Password",
		validators=[
			DataRequired(),
			EqualTo(
				"password",
				message="Password desn't match with confirm password",
			),
		],
	)
	billing_address = StringField(
		"Billing Address",
		validators=[DataRequired(), Length(min=3, max=80)],
	)
	shipping_address = StringField(
		"Shipping Address",
		validators=[DataRequired(), Length(min=3, max=80)],
	)
	# TODO: better validator
	zip_code = IntegerField(
		"Zip Code",
		validators=[
			DataRequired(),
			NumberRange(min=9999, message="Zip Code must be 5 digit"),
		],
	)
	accept_tos = BooleanField("", validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)

	def validate(self, **kwargs):
		initial_validation = super(SignupForm, self).validate()
		if not initial_validation:
			return False
		user = User.query.filter_by(username=self.username.data).first()
		if user:
			self.username.errors.append("Username already registered")
			return False
		email = User.query.filter_by(email=self.email.data).first()
		if email:
			self.email.errors.append("Email already registered")
			return False
		return True


class LoginForm(FlaskForm):
	username = StringField(
		"Username/Email", validators=[DataRequired(), email_or_username()]
	)
	password = PasswordField(
		"Password", validators=[DataRequired(), Length(min=8, max=40)]
	)

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)

	def validate(self, **kwargs):
		initial_validation = super(LoginForm, self).validate()
		if not initial_validation:
			return False

		user = None
		if not username_regex.search(self.username.data):
			user = User.query.filter_by(username=self.username.data).first()
		elif "@" in self.username.data and "." in self.username.data:
			user = User.query.filter_by(email=self.username.data).first()
		if not user:
			self.username.errors.append("User/Email not registered")
			return False
		if not user.check_password(self.password.data):
			self.password.errors.append("Incorrect password")
			return False
		return True
