from datetime import datetime, timezone

from sqlalchemy.ext.associationproxy import association_proxy

from app.database import Column, db


# user One to many Review and product one to many Review
class Review(db.Model):
	id = Column(db.Integer, primary_key=True, autoincrement=True)
	comment = Column(db.String(500))
	rating = Column(db.Integer)
	created_at = Column(
		db.DateTime, nullable=False, default=datetime.now(timezone.utc)
	)

	user_id = Column(db.Integer, db.ForeignKey("user.id"))
	product_id = Column(db.Integer, db.ForeignKey("product.id"))

	user = db.relationship("User", back_populates="reviews", uselist=False)
	product = db.relationship(
		"Product", back_populates="reviews", uselist=False
	)

	def __repr__(self):
		return f"<Review({self.id})>"


class Order(db.Model):
	id = Column(db.Integer, primary_key=True, autoincrement=True)
	# TODO: Order Details and add UUID
	payment_method = Column(db.String(20))
	payment_done = Column(db.Integer)
	status = Column(db.String(30))
	created_at = Column(
		db.DateTime, nullable=False, default=datetime.now(timezone.utc)
	)

	user_id = Column(db.Integer, db.ForeignKey("user.id"))
	address_id = Column(db.Integer, db.ForeignKey("address.id"))

	user = db.relationship("User", back_populates="orders", uselist=False)
	address = db.relationship("Address", uselist=False)

	ordered_product = db.relationship(
		"OrderedProduct", back_populates="order", cascade="all, delete-orphan"
	)
	products = association_proxy(
		"ordered_product",
		"product",
		creator=lambda product_obj: OrderedProduct(product=product_obj),
	)

	def __repr__(self):
		return f"<Order({self.id})>"


class OrderedProduct(db.Model):
	order_id = Column(db.Integer, db.ForeignKey("order.id"), primary_key=True)
	product_id = Column(
		db.Integer, db.ForeignKey("product.id"), primary_key=True
	)
	quantity = Column(db.Integer)

	order = db.relationship("Order", back_populates="ordered_product")
	product = db.relationship("Product")

	def __repr__(self):
		return f"<Ordered Product({self.order_id}, {self.product_id})>"


# Can Also Create Association Proxy Like Order (if need for quantity attribute)
# Otherwise this will suffice
wishlist = db.Table(
	"wishlist",
	Column("user_id", db.ForeignKey("user.id"), primary_key=True),
	Column(
		"product_id",
		db.ForeignKey("product.id", ondelete="CASCADE"),
		primary_key=True,
	),
)

cart = db.Table(
	"cart",
	Column("user_id", db.ForeignKey("user.id"), primary_key=True),
	Column(
		"product_id",
		db.ForeignKey("product.id", ondelete="CASCADE"),
		primary_key=True,
	),
)

# class OrderStatus(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     # TODO: enum (placed, processing, dispatched, last_mile, in_route,
# 	  # refund, return)
#
#     status = db.Column(db.Integer)

# class OrderPayment(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
