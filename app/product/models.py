from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy_utils import aggregated

from app.database import Column, db
from app.models import Review


class Product(db.Model):
	id = Column(db.Integer, primary_key=True, autoincrement=True)
	name = Column(db.String(30), nullable=False)
	description = Column(db.String(150), nullable=False)
	price = Column(db.Integer, nullable=False)
	image = Column(db.String(200), nullable=False)
	stock = Column(db.Integer, nullable=False)
	brand = Column(db.String(50))
	added_on = Column(
		db.DateTime, nullable=False, default=datetime.now(timezone.utc)
	)

	category_id = Column(db.Integer, db.ForeignKey("category.id"))

	category = db.relationship("Category", viewonly=True)
	reviews = db.relationship(
		"Review", back_populates="product", cascade="all, delete-orphan"
	)

	# wishlist_users = db.relationship(
	#  	"User", secondary=wishlist, back_populates="wishlist_products"
	# )
	# cart_users = db.relationship(
	# 	"User", secondary=cart, back_populates="cart_products"
	# )

	def __repr__(self):
		return f"<Product({self.name!r})>"

	@aggregated("reviews", Column(db.Integer))
	def average_rating(self):
		return func.avg(Review.rating)

	@aggregated("reviews", Column(db.Integer))
	def rating_count(self):
		return func.count(Review.comment)


class Category(db.Model):
	id = Column(db.Integer, primary_key=True, autoincrement=True)
	category = Column(db.String(50))

	def __repr__(self):
		return f"<Category({self.category!r})>"


# class ProductVariant(db.Model):
#     id = Column(db.Integer, primary_key=True, autoincrement=True)
#     product_id = Column(db.Integer, db.ForeignKey("product.id"))
