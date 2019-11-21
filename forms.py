from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class VisitorForm(Form):
    name = TextField(
        'Name', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    phone = TextField(
        'Phone', validators=[DataRequired(), Length(min=10, max=40)]
    )


class HostForm(Form):
    name = TextField(
        'Name', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    phone = TextField(
        'Phone', validators=[DataRequired(), Length(min=10, max=40)]
    )
