from flask import Blueprint, Response, render_template, request, session
from flask_login import current_user, login_required

from app.product.models import Product

bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route("/cart", methods=["GET", "DELETE"])
@bp.route("/cart/<int:product_id>", methods=["POST", "DELETE"])
@login_required
def cart(product_id=None):
	# TODO: check product stock if less then 5 or out of stock show to user
	# TODO: validation for product id(s)
	cart = current_user.cart_products
	if product_id:
		product = Product.query.get(product_id)
		if request.method == "POST" and product not in cart:
			current_user.add_to_cart(product)
			session["cart_products"] = len(current_user.cart_products)
		elif request.method == "DELETE" and product in cart:
			current_user.remove_from_cart(product)
			session["cart_products"] = len(current_user.cart_products)
		return Response(status=204)
	elif request.method == "DELETE":
		current_user.clear_cart()
		session["cart_products"] = len(current_user.cart_products)
		return Response(status=204)
	cart_total = sum(product.current_price for product in cart)
	return render_template(
		"user_profile/cart.html", products=cart, cart_total=cart_total
	)


@bp.route("/wishlist", methods=["GET", "POST", "DELETE"])
@bp.route("/wishlist/<int:product_id>", methods=["POST", "DELETE"])
@login_required
def wishlist(product_id=None):
	wishlist = current_user.wishlist_products
	if product_id:
		product = Product.query.get(product_id)
		if request.method == "POST":
			current_user.add_to_wishlist(product)
		elif request.method == "DELETE":
			if product in wishlist:
				current_user.remove_from_wishlist(product)
		return Response(status=204)
	elif request.method == "DELETE":
		current_user.clear_wishlist()
		return Response(status=204)
	elif request.method == "POST":
		product_ids = request.form.getlist("product")
		if product_ids:
			products = [Product.query.get(id) for id in product_ids]
			current_user.move_to_cart(products)
			session["cart_products"] = len(current_user.cart_products)
			return render_template(
				"user_profile/wishlist.html",
				products=current_user.wishlist_products,
			)
		return Response(status=204)
	return render_template("user_profile/wishlist.html", products=wishlist)


@bp.route("/past_orders")
@login_required
def past_orders():
	product_ids = [r.product_id for r in current_user.reviews]
	return render_template(
		"user_profile/past_orders.html",
		orders=current_user.orders,
		r_pids=product_ids,
	)


@bp.route("/details", methods=["GET", "POST"])
@login_required
def user_details():
	if request.method == "POST":
		pass
	return render_template("user_profile/user_details.html")
