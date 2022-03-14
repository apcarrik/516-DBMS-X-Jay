from flask import render_template

from flask import Blueprint
bp = Blueprint('products', __name__)


@bp.route('/productdetails/<int:pid>', methods=['GET', 'POST'])
def details(pid):
    return render_template('productdetails.html', pid=pid)
