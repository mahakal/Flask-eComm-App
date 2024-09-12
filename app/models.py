import secrets
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

	user_id = Column(db.Integer, db.ForeignKey("users.id"))
	product_id = Column(db.Integer, db.ForeignKey("product.id"))

	user = db.relationship("Users", back_populates="reviews", uselist=False)
	product = db.relationship(
		"Product", back_populates="reviews", uselist=False
	)

	def __repr__(self):
		return f"<Review({self.id})>"


class Order(db.Model):
	id = Column(db.Integer, primary_key=True, autoincrement=True)
	order_id = Column(
		db.String(32), unique=True, default=lambda: secrets.token_hex(8).upper()
	)
	subtotal = Column(db.Float, nullable=False)
	shipping = Column(db.Float)
	discount = Column(db.Float)
	tax = Column(db.Float)
	total = Column(db.Float, nullable=False)
	payment_method = Column(db.String(20))
	payment_done = Column(db.Boolean)
	payment_status = Column(db.String(30))
	order_status = Column(db.String(30), default="placed")
	order_note = Column(db.String(500))
	created_at = Column(
		db.DateTime, nullable=False, default=datetime.now(timezone.utc)
	)
	updated_at = Column(
		db.DateTime,
		default=datetime.now(timezone.utc),
		onupdate=datetime.now(timezone.utc),
	)

	user_id = Column(db.Integer, db.ForeignKey("users.id"))
	address_id = Column(db.Integer, db.ForeignKey("address.id"))

	user = db.relationship("Users", back_populates="orders", uselist=False)
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
	sku = Column(db.String(100))
	price = Column(db.Float)
	quantity = Column(db.Integer, default=1)
	subtotal = Column(db.Float)
	discount = Column(db.Float)
	tax = Column(db.Float)
	total = Column(db.Float)

	created_at = Column(
		db.DateTime, nullable=False, default=datetime.now(timezone.utc)
	)
	updated_at = Column(
		db.DateTime,
		default=datetime.now(timezone.utc),
		onupdate=datetime.now(timezone.utc),
	)

	order_id = Column(db.Integer, db.ForeignKey("order.id"), primary_key=True)
	product_id = Column(
		db.Integer, db.ForeignKey("product.id"), primary_key=True
	)

	order = db.relationship("Order", back_populates="ordered_product")
	product = db.relationship("Product")

	def __repr__(self):
		return f"<Ordered Product({self.order_id}, {self.product_id})>"


# Can Also Create Association Proxy Like Order (if need for quantity attribute)
# Otherwise this will suffice
wishlist = db.Table(
	"wishlist",
	Column("user_id", db.ForeignKey("users.id"), primary_key=True),
	Column(
		"product_id",
		db.ForeignKey("product.id", ondelete="CASCADE"),
		primary_key=True,
	),
)

cart = db.Table(
	"cart",
	Column("user_id", db.ForeignKey("users.id"), primary_key=True),
	Column(
		"product_id",
		db.ForeignKey("product.id", ondelete="CASCADE"),
		primary_key=True,
	),
)

# class OrderStatus(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     # TODO: enum (placed, cancelled, processing, dispatched, last_mile,
# 	  # in_route, delivered, refund, return)
#
#     status = db.Column(db.Integer)

# class OrderPayment(db.Model):
# 	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
# 	TODO: enum (cash_on_delivery, net_banking, debit_card, e-wallet)
# 	method:
# 	payment_done: boolean
# 	TODO: enum (waiting, confirmed, failed, cancelled)
# 	status:
