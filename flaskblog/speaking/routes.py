from flask import render_template, Blueprint, flash, redirect, url_for, request, jsonify
from flask_login import login_required
from flaskblog.speaking.forms import SpeakForm, RecodingForm
from flaskblog.speaking.utils import Someaudio, record
from flaskblog import db
from flaskblog.models import Speaking, Speakinganswer
from flask_login import current_user
import speech_recognition as sr
import os

speaking = Blueprint('speaking', __name__)


@speaking.route("/speaking")
def speak():
    speakings = Speaking.query.all()
    return render_template('speaking.html', speakings=speakings)


@speaking.route("/speaking/new", methods=['GET', 'POST'])
@login_required
def new_speaking():
    form = SpeakForm()
    if form.validate_on_submit():
        que_01 = Someaudio(form.question_01.data)
        que_02 = Someaudio(form.question_02.data)
        que_03 = Someaudio(form.question_03.data)
        que_04 = Someaudio(form.question_04.data)
        que_05 = Someaudio(form.question_05.data)
        speak = Speaking(title=form.title.data, question_01=que_01, question_02=que_02,
                         question_03=que_03, question_04=que_04, question_05=que_05, vspeak=current_user)
        db.session.add(speak)
        db.session.commit()
        flash('Your Speaking Paper has been Created!', 'success')
        return redirect(url_for('speaking.speak'))
    return render_template('create_speak.html', title='Speaking Paper', form=form, legend='Speaking Paper')


@speaking.route("/speaking/<int:speaking_id>", methods=['GET', 'POST'])
@login_required
def show_speaking(speaking_id):
    speak = Speaking.query.get_or_404(speaking_id)
    form = RecodingForm()
    speaksA = Speakinganswer.query.all()
    print(speaksA[-1])
    print(speaksA[-1].id + 1)

    if form.is_submitted():
        x = 0
        print(x)
        while(x == 0):
            speaks = Speakinganswer(id=speaksA[-1].id + 1,
                                    pid=speaking_id, speakanswer=current_user)
            db.session.add(speaks)
            db.session.commit()
            x = x+1

        if form.record1.data:
            file_name1 = record(5)
            print(file_name1)
            print(speaksA[-1].id + 1)
            if (file_name1 != 'none'):
                speaks.id = speaksA[-1].id + 1
                speaks.pid = speaking_id
                speaks.answer_01 = file_name1
                speaks.speakanswer = current_user
                db.session.commit()
            file_name2 = "none"
            file_name3 = "none"
            file_name4 = "none"
            file_name5 = "none"
        elif form.record2.data:
            file_name2 = record(5)
            file_name1 = "none"
            file_name3 = "none"
            file_name4 = "none"
            file_name5 = "none"
        elif form.record3.data:
            file_name3 = record(5)
            file_name2 = "none"
            file_name1 = "none"
            file_name4 = "none"
            file_name5 = "none"
        elif form.record4.data:
            file_name4 = record(5)
            file_name2 = "none"
            file_name3 = "none"
            file_name1 = "none"
            file_name5 = "none"
        elif form.record5.data:
            file_name5 = record(5)
            file_name2 = "none"
            file_name3 = "none"
            file_name4 = "none"
            file_name1 = "none"
        return render_template('speaking_paper.html',  speak=speak, file_name1=file_name1, file_name2=file_name2, file_name3=file_name3, file_name4=file_name4, file_name5=file_name5, form=form)
    file_name1 = "none"
    file_name2 = "none"
    file_name3 = "none"
    file_name4 = "none"
    file_name5 = "none"
    return render_template('speaking_paper.html',  speak=speak, file_name1=file_name1, file_name2=file_name2, file_name3=file_name3, file_name4=file_name4, file_name5=file_name5, form=form)
