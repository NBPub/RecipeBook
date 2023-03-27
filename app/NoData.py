from flask import Blueprint, render_template
from .__init__ import data_path

bp = Blueprint('NoData', __name__, url_prefix='/')
# Error page for data loading
@bp.route("/", methods = ['GET'])
@bp.route("/recipes/", methods = ['GET'])
def homepage():
    return render_template('NoData.html', data_path=data_path)