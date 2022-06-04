from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LandingForm(FlaskForm):
    user = StringField("Username...", render_kw={"Placeholder" : "Channel's username..."})
    submit = SubmitField()