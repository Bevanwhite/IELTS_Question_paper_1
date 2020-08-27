from flask import Blueprint, render_template

listening = Blueprint('listening', __name__)


@listening.route("/listening")
def listen():
    return render_template('listening.html')
