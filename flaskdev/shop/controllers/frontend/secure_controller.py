from flask import flash, render_template,Blueprint,redirect,url_for, session
from flask_mail import Message
from shop.config import Tao_mat_khau
from shop.models.account import Account
from shop.forms.form_account import RegisterForm,LoginForm,ForgetForm
from shop import db,bcrypt,login_manager,mail,google
from flask_login import login_user,logout_user

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))


secure_route = Blueprint('secure', __name__)

@secure_route.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        account=Account(fullname=form.fullname.data,email=form.email.data,password= bcrypt.generate_password_hash(form.password.data),phone=form.phone.data,image='avatar.png',role='user')
        db.session.add(account)
        db.session.commit()
        flash('Account created successfully','success')
        return redirect(url_for('secure.login'))
    return render_template('secure/pages/register.html',form=form)

@secure_route.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(email=form.email.data).first()

        # Kiểm tra thông tin đăng nhập
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash('Đăng nhập thành công', 'success')
            return redirect(url_for('home.index'))
        else:
            flash('Email hoặc mật khẩu không đúng', 'danger')

    

    return render_template('secure/pages/login.html', form=form)
    
@secure_route.route('/logout')
def logout():
    logout_user()
    flash('Đăng xuất thành công', 'success')
    return redirect(url_for('home.index'))



@secure_route.route("/forget",methods=['GET','POST'])
def forget():
    form=ForgetForm()
    if form.validate_on_submit():
        #gửi mật khẩu khôi phục qua email
        email=form.email.data
        phone=form.phone.data
        user=Account.query.filter_by(email=email).first()
        if user and user.phone==phone:
            #tạo mật khẩu và mã hóa lưu vào cơ csdl
            newpass=Tao_mat_khau() #pass mới không mã hóa
            user.password=bcrypt.generate_password_hash(newpass).decode('utf-8')
            db.session.commit()

            #gửi mật khẩu mới không bị mã hóa đi
            msg=Message("Mật khẩu mới của bạn: ",recipients=[email])
            msg.body=f"Xin chào {user.fullname}, \n\n Mật khẩu mới của bạn là: {newpass} \n Vui lòng đăng nhập và đổi mật khẩu. \n\n Trân trọng, \n Đội ngũ hỗ trợ."
            mail.send(msg)
            flash("Mật khẩu mới đã được gửi tới email của bạn",'success')
            return redirect(url_for("secure.login"))
        else:
            flash("Thông tin tài khoản không chính xác",'error')   

    return render_template("secure/pages/forget.html",form=form)


@secure_route.route("/gmail",methods=['GET','POST'])
def gmail():
    
    return google.authorize_redirect(url_for('secure.gmail_auth', _external=True))

@secure_route.route("/gmail/auth",methods=['GET','POST'])
def gmail_auth():
    token = google.authorize_access_token()
    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    info = google.get(user_info_url).json()
    
    hoten = info['name']
    email = info['email']
    avatar = info['picture']

    taikhoan = Account.query.filter_by(email=email).first()
    if not taikhoan:
        taikhoan=Account(
            fullname=hoten,
            email=email,
            password='',
            phone='0123456789',
            image=avatar,
            role='user',
            is_active=1,

        )
        db.session.add(taikhoan)
        db.session.commit()
    login_user(taikhoan)
    return redirect(url_for('home.index'))
    
@secure_route.route('/set_test_session')
def set_test_session():
    session['test_key'] = 'test_value'
    return "Session set!"

@secure_route.route('/get_test_session')
def get_test_session():
    return session.get('test_key', "Session not found")
