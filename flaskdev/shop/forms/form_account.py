from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField,SubmitField,PasswordField
from wtforms.validators import DataRequired, Length,Email,Regexp,ValidationError
from shop.models.account import Account

class RegisterForm(FlaskForm):
    fullname=StringField(
        "Full name", 
        validators=[
            DataRequired(message='Vui lòng không để trống'),
            Length(min=6,max=160,message='Nhập từ 6 - 32 ký tự')
        ],
        render_kw={'class':'form-control','placeholder':'Enter full name'} #thêm class form-control
    )
    email=StringField(
        "Email", 
        validators=[
            DataRequired(message='Vui lòng không để trống'),
            Email()
        ],
        render_kw={'class':'form-control','placeholder':'Enter email'} 
    )
    password=PasswordField(
        "Password", 
        validators=[
            DataRequired(message='Vui lòng không để trống'),
            Length(min=6,max=32,message='Nhập từ 6 - 32 ký tự'),
            Regexp('^[a-zA-Z0-9]*$',message='Password chỉ được phép nhập ký tự và số')
        ],
        render_kw={'class':'form-control','placeholder':'Enter Password'} 
    )
    phone=StringField(
        "Phone", 
        validators=[
            DataRequired(message='Vui lòng không để trống'),
            Length(min=10,max=12,message='Nhập từ 10 - 12 số'),
            Regexp('^[0-9]*$',message='Password chỉ được phép nhập số')
        ],
        render_kw={'class':'form-control','placeholder':'Enter email'} 
    )
    submit=SubmitField(
        'Đăng Ký',
        render_kw={'class':'btn btn-primary btn-sm'} 
    )

    def validate_email(self,email):
        if Account.query.filter_by(email=email.data).first():
            raise ValidationError("Email đã tồn tại, vui lòng nhập email khác")


class LoginForm(FlaskForm):
    email=StringField(
        "Email", 
        validators=[
            DataRequired(message='Vui lòng không để trống'),
            Email()
        ],
        render_kw={'class':'form-control','placeholder':'Enter email'} 
    )
    password=PasswordField(
        "Password", 
        validators=[
            DataRequired(message='Vui lòng không để trống'),
            Length(min=6,max=32,message='Nhập từ 6 - 32 ký tự'),
            Regexp('^[a-zA-Z0-9]*$',message='Password chỉ được phép nhập ký tự và số')
        ],
        render_kw={'class':'form-control','placeholder':'Enter Password'} 
    )
    remember=BooleanField('Remember',default=False)
    submit=SubmitField(
        'Đăng nhập',
        render_kw={'class':'btn btn-primary btn-sm'} 
    )


class ForgetForm(FlaskForm):
    email=StringField(
        "Email", 
        validators=[
            DataRequired(message='Vui lòng không để trống'),
            Email()
        ],
        render_kw={'class':'form-control','placeholder':'Enter email'} 
    )
    phone=StringField(
        "Phone", 
        validators=[
            DataRequired(message='Vui lòng không để trống'),
            Length(min=6,max=32,message='Nhập từ 10-12 ký tự'),
            Regexp('^[0-9]*$',message='Điện thoại chỉ được phép nhập số')
        ],
        render_kw={'class':'form-control','placeholder':'Enter Phone'} 
    )
    remember=BooleanField('Remember',default=True)
    submit=SubmitField(
        'Khôi phục',
        render_kw={'class':'btn btn-primary btn-sm'} 
    )