from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired, NumberRange

class LoginForm(FlaskForm):
    username = StringField("Käyttäjä", validators=[DataRequired()])
    pin = IntegerField("PIN", validators=[DataRequired()])
    submit = SubmitField("Kirjaudu")

class ReviewForm(FlaskForm):
    melody = IntegerField("Melodia", validators=[DataRequired(), NumberRange(min=4, max=10)])
    performance = IntegerField("Esiintyminen", validators=[DataRequired(), NumberRange(min=4, max=10)])
    wardrobe = IntegerField("Asu", validators=[DataRequired(), NumberRange(min=4, max=10)])
    submit = SubmitField("Tallenna")