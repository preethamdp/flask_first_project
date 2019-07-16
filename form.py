from flask-wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired,Length

class simpleForm(FlaskForm):
    search_string = StringField('search',validators=[DataRequired(),Length(min=2,max=20)])
    submit = SubmitField('submit')
