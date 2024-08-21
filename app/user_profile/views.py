from flask import Blueprint, Response, render_template, request
from flask_login import current_user, login_required

from app.product.models import Product

bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route("/cart", methods=["GET", "DELETE"])
@bp.route("/cart/<int:product_id>", methods=["POST", "DELETE"])
@login_required
def cart(product_id=None):
	# TODO: check product stock if less then 5 or out of stock show to user
	cart = current_user.cart_products
	if product_id:
		product = Product.query.get(product_id)
		if request.method == "POST":
			current_user.add_to_cart(product)
		elif request.method == "DELETE":
			if product in cart:
				current_user.remove_from_cart(product)
		return Response(status=204)
	if request.method == "DELETE":
		current_user.clear_cart()
		return Response(status=204)
	return render_template("user_profile/cart.html", products=cart)


@bp.route("/wishlist", methods=["GET", "DELETE"])
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
	if request.method == "DELETE":
		current_user.clear_wishlist()
		return Response(status=204)
	return render_template("user_profile/wishlist.html", products=wishlist)


@bp.route("/past_orders")
@login_required
def past_orders():
	product_ids = [r.product_id for r in current_user.reviews]
	print(product_ids)
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
