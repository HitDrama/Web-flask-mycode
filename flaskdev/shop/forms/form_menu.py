from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField,SubmitField
from wtforms.validators import DataRequired, Length,NumberRange

class MenuForm(FlaskForm):
    name=StringField(
        "Tên menu", 
        validators=[DataRequired(),Length(min=3,max=160)],
        render_kw={'class':'form-control'} #thêm class form-control
    )
    url=StringField(
        "Url", 
        validators=[DataRequired()],
        render_kw={'class':'form-control'} #thêm class form-control
    )
    order=IntegerField(
        "Thứ tự", 
        validators=[DataRequired(),NumberRange(min=0)],
        render_kw={'class':'form-control'} #thêm class form-control
    )
    is_active=BooleanField('Kích hoạt',default=True)
    parent_id=SelectField(
        "Menu cha", 
        coerce=int,
        default=0,
        render_kw={'class':'form-control'} #thêm class form-control
    )
    submit=SubmitField(
        'Save',
        render_kw={'class':'btn btn-primary btn-sm'} 
    )