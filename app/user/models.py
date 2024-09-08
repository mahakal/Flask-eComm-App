# import uuid

from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy_utils import UUIDType


from app.database import Column, db
from app.extensions import bcrypt
from app.models import cart, wishlist


class Users(UserMixin, db.Model):
	id = Column(db.Integer, primary_key=True, autoincrement=True)
	# s_id = Column(UUIDType(), default=uuid.uuid4, unique=True)
	first_name = Column(db.String(30), nullable=False)
	last_name = Column(db.String(30), nullable=False)
	dob = Column(db.Date, nullable=False)
	username = Column(db.String(50), unique=True, nullable=False)
	email = Column(db.String(80), unique=True, nullable=False)
	country_code = Column(db.String(10), nullable=False)
	mobile_number = Column(db.String(15))
	_password = Column("password", db.LargeBinary(128), nullable=True)

	created_at = Column(
		db.DateTime, nullable=False, default=datetime.now(timezone.utc)
	)

	accept_tos = Column(db.Boolean)
	is_active = Column(db.Boolean, default=False)
	is_admin = Column(db.Boolean, default=False)

	addresses = db.relationship("Address")
	active_address = db.relationship(
		"Address",
		uselist=False,
		primaryjoin="and_(Users.id==Address.user_id, Address.is_active==True)",
		viewonly=True,
	)
	reviews = db.relationship("Review", back_populates="user")
	wishlist_products = db.relationship("Product", secondary=wishlist)
	cart_products = db.relationship("Product", secondary=cart)
	orders = db.relationship("Order", back_populates="user")

	# wishlist_products = db.relationship(
	# 	"Product", secondary=wishlist, back_populates="wishlist_users"
	# )
	# cart_products = db.relationship(
	# 	"Product", secondary=cart, back_populates="cart_users"
	# )

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

	def _add_to_relation(self, relation, data_inst):
		getattr(self, relation).append(data_inst)
		db.session.add(self)
		db.session.commit()

	def _remove_from_relation(self, relation, data_inst):
		getattr(self, relation).remove(data_inst)
		db.session.add(self)
		db.session.commit()

	def _clear_relation(self, relation):
		getattr(self, relation).clear()
		db.session.add(self)
		db.session.commit()

	def add_to_cart(self, product):
		self._add_to_relation("cart_products", product)

	def remove_from_cart(self, product):
		self._remove_from_relation("cart_products", product)

	def clear_cart(self):
		self._clear_relation("cart_products")

	def add_to_wishlist(self, product):
		self._add_to_relation("wishlist_products", product)

	def remove_from_wishlist(self, product):
		self._remove_from_relation("wishlist_products", product)

	def clear_wishlist(self):
		self._clear_relation("wishlist_products")

	def add_to_order(self, order):
		self._add_to_relation("order", order)

	def remove_from_order(self, order):
		self._remove_from_relation("order", order)

	def move_to_cart(self, products):
		self.cart_products.extend(
			product
			for product in products
			if product not in self.cart_products
		)
		for product in products:
			if product in self.wishlist_products:
				self.remove_from_wishlist(product)
		db.session.add(self)
		db.session.commit()


class Address(db.Model):
	id = Column(db.Integer, primary_key=True, autoincrement=True)

	billing_address = Column(db.String(80), nullable=False)
	shipping_address = Column(db.String(80), nullable=False)
	zip_code = Column(db.Integer, nullable=False)
	is_active = Column(db.Boolean)

	user_id = Column(db.Integer, db.ForeignKey("users.id"))
