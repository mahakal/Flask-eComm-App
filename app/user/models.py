from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from app.database import db, Column
from app.extensions import bcrypt

class User(UserMixin, db.Model):
    
    id = Column(db.Integer(), primary_key=True, autoincrement=True)
    first_name = Column(db.String(30), nullable=False)
    last_name = Column(db.String(30), nullable=False)
    dob = Column(db.Date(), nullable=False)
    username = Column(db.String(50), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    country_code = Column(db.String(10), nullable=False)
    mobile_number = Column(db.String(15))
    _password = Column("password", db.LargeBinary(128), nullable=True)
    billing_address = Column(db.String(80), nullable=False)
    shipping_address = Column(db.String(80), nullable=False)
    zip_code = Column(db.Integer(), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    accept_tos = Column(db.Boolean())
    is_active = Column(db.Boolean(), default=False)
    is_admin = Column(db.String(80), default=False)
    
    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = bcrypt.generate_password_hash(value)
    
    def check_password(self, value):
        return bcrypt.check_password_hash(self._password, value)
    
    def __repr__(self):
        return f"<User({self.username!r})>"
