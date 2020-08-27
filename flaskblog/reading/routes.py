from flask import render_template, Blueprint

reading = Blueprint('reading', __name__)


@reading.route("/reading")
def read():
    return render_template('reading.html')
