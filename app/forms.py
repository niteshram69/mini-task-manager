from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(message="Title is required"),
        Length(min=1, max=100, message="Title must be between 1 and 100 characters")
    ])
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=500, message="Description must be less than 500 characters")
    ])
    completed = BooleanField('Completed')
    submit = SubmitField('Save Task')
