from flask import render_template, Blueprint
from flask_login import login_required

speaking = Blueprint('speaking', __name__)


@speaking.route("/speaking")
def speak():
    return render_template('speaking.html')


@speaking.route("/speaking/new")
@login_required
def new_speaking():
    pass
