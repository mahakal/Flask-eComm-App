from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from app.database import db, Column


class Product(db.Model):

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    name = Column(db.String(30), nullable=False)
    description = Column(db.String(150), nullable=False)
    price = Column(db.Integer, nullable=False)
    average_rating = Column(db.Integer)
    brand_name = Column(db.String(50))
    added_on = Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    category_id = Column(db.Integer, db.ForeignKey("category.id"))

    review = db.relationship("Review", back_populates="product", cascade="all, delete-orphan")

    # wishlist_users = db.relationship("User", secondary=wishlist, back_populates="wishlist_products")
    # cart_users = db.relationship("User", secondary=cart, back_populates="cart_products")

    def __repr__(self):
        return f"<Product({self.name!r})>"


class Category(db.Model):

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    name = Column(db.String(50))

    def __repr__(self):
        return f"<Category({self.category!r})>"
