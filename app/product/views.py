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
from app.models import Order, OrderedProduct, Review

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
	ids = request.form.getlist("product")
	print(ids)
	checkout = [{"id": id, "quantity": request.form.get(id, "")} for id in ids]
	# checkout = [(id, request.form.get(id, "")) for id in ids]
	checkout = []
	for id in ids:
		_q = request.form.get(id, "")
		if _q and _q.isdigit() and 1 <= int(_q):
			_q = int(_q)
		else:
			_q = 1
		checkout.append({"id": id, "quantity": _q})
	if ids:
		products = [Product.query.get(product_id) for product_id in ids]
		total = sum(map(lambda x: x.price, products))
		session["checkout"] = checkout
		return render_template(
			"product/checkout.html", products=products, total=total
		)
	return Response(status=204)


@bp.route("/order", methods=["POST"])
@login_required
def order():
	checkout_lines = session.get("checkout")
	payment_method = request.form.get("method")
	quantity = 1
	if payment_method:
		subtotal = 0
		products = []
		ordered_products = []
		for checkout_line in checkout_lines:
			_p = Product.query.get(checkout_line["id"])
			quantity = checkout_line["quantity"]
			ordered_product = OrderedProduct(
				sku=_p.sku,
				price=_p.current_price,
				quantity=quantity,
				subtotal=_p.current_price * quantity,
				discount=_p.price - _p.sale_price,
				total=(_p.current_price * quantity)
				- (_p.price - _p.sale_price)
				+ _p.tax,
			)
			subtotal += _p.current_price * quantity
			_p.stock -= quantity
			products.append(_p)
			ordered_product.product = _p
			ordered_products.append(ordered_product)
		db.session.add_all(products)
		order = Order(
			subtotal=subtotal,
			total=subtotal,
			payment_method=payment_method,
			payment_done=0,
			payment_status="confirmed",
			user=current_user,
			address=current_user.active_address,
			ordered_product=ordered_products,
		)
		current_user.cart_products = [
			_cp for _cp in current_user.cart_products if _cp not in products
		]
		session["cart_products"] = len(current_user.cart_products)
		current_user.wishlist_products = [
			_wp
			for _wp in current_user.wishlist_products
			if _wp not in products
		]
		db.session.add(order)
		db.session.commit()

		return render_template("product/order.html", products=products)
	return Response(status=204)


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
