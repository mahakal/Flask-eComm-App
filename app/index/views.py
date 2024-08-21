from flask import Blueprint, render_template

from app.product.models import Product

bp = Blueprint("index", __name__)


@bp.route("/", methods=["GET"])
def index():
	products = Product.query.order_by("id").limit(20).all()
	return render_template("index/index.html", products=products)
