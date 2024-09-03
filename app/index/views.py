from flask import Blueprint, render_template, request

from app.product.models import Product

bp = Blueprint("index", __name__)


@bp.route("/", methods=["GET"])
def index():
	products = Product.query.order_by("id").limit(20).all()
	page = request.args.get("page", 1, type=int)
	products = Product.query.order_by(Product.added_on.desc()).paginate(
		page=page, per_page=10
	)
	return render_template(
		"index/index.html", products=products.items, pagination=products
	)
