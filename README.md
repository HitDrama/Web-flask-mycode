# Flask Shop - Online Course on AI by MYCODE

## Giới thiệu

Dự án này là một khóa học trong chương trình đào tạo Trí tuệ Nhân tạo tại MYCODE. Web app được xây dựng bằng Flask, với template frontend và backend lấy từ [Themewagon](https://themewagon.com/).

Dự án này cung cấp một nền tảng học trực tuyến, cho phép người dùng đăng ký, đăng nhập, và học các khóa học về trí tuệ nhân tạo.

- **Backend**: Flask
- **Frontend**: Template lấy từ Themewagon
- **Cơ sở dữ liệu**: MySQL

Website này là một phần của chương trình học tại [MYCODE](https://www.mycode.edu.vn).

## Cấu hình dự án

### Lưu ý

Dự án này thiếu file cấu hình `config.py`, trong đó chứa các thông tin quan trọng như OAuth và cấu hình SMTP. Bạn cần phải tạo và cấu hình file `config.py` để dự án hoạt động đúng.

### Hướng dẫn cấu hình file `config.py`

1. Tạo file cấu hình `config.py` tại đường dẫn `flaskdev/shop/config.py` trong dự án của bạn.

2. Nội dung của file `config.py` như sau:

```python
import os
import string
import random

class Config:
    SECRET_KEY = os.urandom(24)  # khóa bảo mật dùng để bảo vệ session và form
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/flaskdev'  # đường dẫn đến cơ sở dữ liệu
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # không theo dõi thay đổi của đối tượng

    
class EmailConfig:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''  # Thay bằng email của bạn
    MAIL_PASSWORD = ''  # Thay bằng mật khẩu email của bạn
    MAIL_DEFAULT_SENDER = ('Flask Shop', 'anhdongden15@gmail.com')

def Tao_mat_khau(length=8):
    kytu = string.ascii_letters + string.digits
    return ''.join(random.choice(kytu) for i in range(length))


class ConfigGmail:
    SECRET_KEY = os.urandom(24)  #Tạo ngẫu nhiên key: chuỗi ngẫu nhiên
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/flaskdev'
    GOOGLE_CLIENT_ID = '' # tạo app trên google cloud
    GOOGLE_CLIENT_SECRET = ''# tạo app trên google cloud
    GOOGLE_ACCESS_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
    GOOGLE_AUTHORIZE_URL = 'https://accounts.google.com/o/oauth2/auth'
    GOOGLE_USERINFO_ENDPOINT = 'https://www.googleapis.com/oauth2/v3/userinfo'
    OAUTHLIB_INSECURE_TRANSPORT = True  # Chỉ sử dụng trong môi trường phát triển
```
Các bước cấu hình:
1. Cấu hình Email:

Điền email và mật khẩu của bạn vào các trường MAIL_USERNAME và MAIL_PASSWORD trong class EmailConfig.
Bạn cần sử dụng Gmail SMTP server nếu sử dụng Gmail để gửi email.
2. Cấu hình OAuth:

Thay GOOGLE_CLIENT_ID và GOOGLE_CLIENT_SECRET bằng thông tin bạn có từ Google Developer Console.
Cấu hình cơ sở dữ liệu:

Thay đổi SQLALCHEMY_DATABASE_URI nếu bạn sử dụng cơ sở dữ liệu khác ngoài MySQL hoặc muốn thay đổi tên cơ sở dữ liệu.
Cài đặt dự án
1. Cài đặt các phụ thuộc Python:
```python
pip install -r requirements.txt
```
2. Chạy ứng dụng Flask:
```python
python app.py
```


