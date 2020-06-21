from flask import render_template, Blueprint

speaking = Blueprint('speaking', __name__)


@speaking.route("/speaking")
def speak():
    return render_template('speaking.html')
