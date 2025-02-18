from shop import db
from datetime import datetime
from flask_login import UserMixin

class Account(db.Model,UserMixin):
    __tablename__="accounts"
    id=db.Column(db.Integer,primary_key=True)
    fullname=db.Column(db.String(150),nullable=False)
    email=db.Column(db.String(150),nullable=False)
    password=db.Column(db.String(150),nullable=False)
    phone=db.Column(db.String(150),nullable=False)
    address=db.Column(db.String(200),nullable=True)
    image=db.Column(db.String(150),nullable=False)
    is_active=db.Column(db.Boolean,default=True)
    role=db.Column(db.String(150),nullable=False)
    create_at=db.Column(db.DateTime,default=datetime.utcnow)
    update_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.now)

    def __repr__(self):
        return f'<Account {self.fullname} >'
    
    def has_role(self, role_name): #dùng kiểm tra quyền khi login
        return self.role==role_name