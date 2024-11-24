from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length

class TransactionForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired(), Length(max=50)])
    amount = FloatField('Amount', validators=[DataRequired()])
    description = StringField('Description', validators=[Length(max=200)])
    submit = SubmitField('Add Transaction')
