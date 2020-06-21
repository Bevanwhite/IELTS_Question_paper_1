from flask import Blueprint

listening = Blueprint('listening', __name__)


@listening.route("/listening")
def listening():
    questions = Questionpaper.query.filter(
        Questionpaper.questiontype.endswith('listening')).all()
    return render_template('listening.html', questions=questions)
