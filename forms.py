from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired


class SearchMovieForm(FlaskForm):
    movie = StringField(label='Movie Title', validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")


class RateMovieForm(FlaskForm):
    my_rating = StringField(label='Your rating out of 10 e.g. 7.5', validators=[DataRequired()])
    submit = SubmitField(label="Done")

