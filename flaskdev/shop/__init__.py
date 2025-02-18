from datetime import timedelta
from flask import Flask,Blueprint, flash, redirect, url_for
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from shop.config import Config,EmailConfig,ConfigGmail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_required,current_user
from authlib.integrations.flask_client import OAuth
from shop.utils import generate_slug
from flask_session import Session
import redis
import os

db = SQLAlchemy()  # Định nghĩa db

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'),static_url_path='/shop/static')

app.secret_key = 'supersecretkey'  # Thay thế bằng một key bảo mật



bcrypt = Bcrypt(app)
login_manager = LoginManager()  # Định nghĩa login manager

#tải cấu hình email vào ứng dụng
app.config.from_object(EmailConfig)
mail = Mail(app)

#đưa hàm generate_slug vào ứng dụng (jinja2)
app.jinja_env.filters['slug'] = generate_slug

#tạo session
sess=Session()
#cài đặt redis
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True # Keep sessions between requests
app.config['SESSION_USE_SIGNER'] = True # Sign session cookies for security
app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6379, db=0)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7) 
sess.init_app(app)


#tải cấu hình API của gmail vào ứng dụng
app.config.from_object(ConfigGmail)
oauth = OAuth(app)

# google = oauth.register(
#     name='google',
#     client_id=Config.GOOGLE_CLIENT_ID,
#     client_secret=Config.GOOGLE_CLIENT_SECRET,
#     access_token_url=Config.GOOGLE_ACCESS_TOKEN_URL,
#     authorize_url=Config.GOOGLE_AUTHORIZE_URL,
#     userinfo_endpoint=Config.GOOGLE_USERINFO_ENDPOINT,
#     client_kwargs={'scope': 'openid profile email'},
# )

google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url=app.config['GOOGLE_ACCESS_TOKEN_URL'],
    authorize_url=app.config['GOOGLE_AUTHORIZE_URL'],
    userinfo_endpoint=app.config['GOOGLE_USERINFO_ENDPOINT'],
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs"
)


def create_app():

    app.config.from_object(Config)  # Tải cấu hình
    db.init_app(app)  # Khởi tạo DB với ứng dụng

    login_manager.init_app(app)  # Khởi tạo login manager
    login_manager.login_view = 'secure.login'  # Đăng nhập bắt buộc

    # route backend
    from shop.controllers.backend.manager_controller import m_route
    from shop.controllers.backend.category_controller import cat_route
    from shop.controllers.backend.product_controller import pro_route
    from shop.controllers.backend.menu_controller import menu_route
    


    sys_route = Blueprint("sys",__name__)
    @sys_route.before_request
    @login_required
    def check_admin():
        if not current_user.has_role('admin'):
            flash('Bạn không có quyền truy cập','danger')
            return redirect(url_for('secure.login'))

    sys_route.register_blueprint(m_route, url_prefix='/manager')
    sys_route.register_blueprint(cat_route, url_prefix='/category')
    sys_route.register_blueprint(pro_route, url_prefix='/product')
    sys_route.register_blueprint(menu_route, url_prefix='/menu')
   
    app.register_blueprint(sys_route, url_prefix='/system')






    # route frontend
    from shop.controllers.frontend.home_controller import h_route
    from shop.controllers.frontend.secure_controller import secure_route
    app.register_blueprint(secure_route, url_prefix='/secure')
    app.register_blueprint(h_route, url_prefix='/')

    return app
