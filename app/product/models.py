from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy_utils import aggregated

from app.database import Column, db
from app.models import Review


class Product(db.Model):
	id = Column(db.Integer, primary_key=True, autoincrement=True)
	name = Column(db.String(200), nullable=False)
	description = Column(db.String(2000), nullable=False)
	price = Column(db.Float, nullable=False)
	tax = Column(db.Float, default=0)
	sold_count = Column(db.Integer, default=0)
	sale_price = Column(db.Float, default=0)
	sale_start_time = Column(db.DateTime)
	sale_end_time = Column(db.DateTime)
	image = Column(db.String(200), nullable=False)
	stock = Column(db.Integer, nullable=False)
	sku = Column(db.String(100), unique=True)
	weight = Column(db.Float)
	dimensions = Column(db.String(100))
	brand = Column(db.String(50))
	added_on = Column(
		db.DateTime, nullable=False, default=datetime.now(timezone.utc)
	)
	updated_at = Column(
		db.DateTime,
		default=datetime.now(timezone.utc),
		onupdate=datetime.now(timezone.utc),
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

	@property
	def is_on_sale(self):
		now = datetime.now(timezone.utc)
		if isinstance(self.sale_start_time, datetime) and isinstance(
			self.sale_end_time, datetime
		):
			return (
				self.sale_price is not None
				and self.sale_start_time <= now <= self.sale_end_time
			)
		else:
			return False

	@property
	def current_price(self):
		return self.sale_price if self.is_on_sale else self.price


class Category(db.Model):
	id = Column(db.Integer, primary_key=True, autoincrement=True)
	category = Column(db.String(50))

	def __repr__(self):
		return f"<Category({self.category!r})>"


# class ProductVariant(db.Model):
#     id = Column(db.Integer, primary_key=True, autoincrement=True)
#     product_id = Column(db.Integer, db.ForeignKey("product.id"))
