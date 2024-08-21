from flask import (
	Blueprint,
	Response,
	redirect,
	render_template,
	request,
	session,
	url_for,
	flash,
)
from flask_login import current_user, login_required
from sqlalchemy_utils import escape_like

from app.database import db
from app.models import Order, Review

from .forms import ReviewForm
from .models import Product

bp = Blueprint("product", __name__, url_prefix="/product")


@bp.route("/<int:product_id>")
def product(product_id):
	# TODO: db.get_or_404(User, id)
	product = Product.query.get(product_id)
	in_cart = (
		True
		if current_user.is_authenticated
		and product in current_user.cart_products
		else False
	)
	in_wishlist = (
		True
		if current_user.is_authenticated
		and product in current_user.wishlist_products
		else False
	)
	return render_template(
		"product/product_page.html",
		product=product,
		in_cart=in_cart,
		in_wishlist=in_wishlist,
	)


@bp.route("/checkout", methods=["POST"])
@login_required
def checkout():
	product_ids = request.form.getlist("product")
	print(product_ids)
	if product_ids:
		products = []
		total = 0
		for product_id in product_ids:
			_p = Product.query.get(product_id)
			total += _p.price
			products.append(_p)
		session["checkout"] = product_ids
		return render_template(
			"product/checkout.html", products=products, total=total
		)
	return Response(204)


@bp.route("/order", methods=["POST"])
@login_required
def order():
	product_ids = session["checkout"]
	if product_ids:
		products = []
		for product_id in product_ids:
			_p = Product.query.get(product_id)
			products.append(_p)
		order = Order(
			payment_method="Cash On Delivery",
			payment_done=0,
			status="processing",
			user=current_user,
			address=current_user.active_address,
			products=products,
		)
		current_user.cart_products = [
			_cp for _cp in current_user.cart_products if _cp not in products
		]
		current_user.wishlist_products = [
			_wp
			for _wp in current_user.wishlist_products
			if _wp not in products
		]
		db.session.add(order)
		db.session.commit()

		return render_template("product/order.html", products=products)


@bp.route("/search", methods=["GET"])
def search():
	query = request.args.get("query", "")
	# empty string returns no products
	if not query:
		_q = ""
	else:
		# escaping wildcards "*, _, %"
		_q = f"%{escape_like(query)}%"
	result = Product.query.filter(Product.name.ilike(_q)).all()
	return render_template("product/search.html", query=query, result=result)


@bp.route("/review/<int:product_id>", methods=["GET", "POST"])
def review(product_id):
	product = Product.query.get(product_id)
	form = ReviewForm(request.form)
	if request.method == "POST" and form.validate_on_submit():
		rating = request.form.get("rating", "")
		print(f"rating {rating}")
		if rating:
			r = Review(
				rating=rating,
				comment=form.comment.data,
				user=current_user,
				product=product,
			)
			db.session.add(r)
			db.session.commit()
			return redirect(url_for("index.index"))
		else:
			flash("Please Provide Star Rating", category="success")
	return render_template(
		"product/review.html",
		reviews=product.reviews,
		product=product,
		form=form,
	)
