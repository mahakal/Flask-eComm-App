from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class ReviewForm(FlaskForm):
	comment = StringField(
		"Comment", validators=[DataRequired(), Length(max=500)]
	)

	def validate(self, **kwargs):
		initial_validation = super(ReviewForm, self).validate()
		if not initial_validation:
			return False
		return True
