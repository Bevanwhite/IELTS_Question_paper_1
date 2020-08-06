from flask import render_template, Blueprint, flash, redirect, url_for, request, jsonify
from flask_login import login_required
from flaskblog.speaking.forms import SpeakForm, RecodingForm
from flaskblog.speaking.utils import Someaudio, record
from flaskblog import db
from flaskblog.models import Speaking, Speakinganswer
from flask_login import current_user
import speech_recognition as sr
import os
import sqlite3
from datetime import datetime
from datetime import timedelta

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
    speaking = Speaking.query.get_or_404(speaking_id)
    form = RecodingForm()

    if form.is_submitted():
        speaks = Speakinganswer.query.all()
        speaking = Speaking.query.get_or_404(speaking_id)
        print(speaks)
        if len(speaks) == 0:
            print('list is empty')
            speak = Speakinganswer(
                id=1, pid=speaking_id, date_posted=datetime.now(), speakanswer=current_user)
            db.session.add(speak)
            db.session.commit()
            conn = sqlite3.connect(
                'C:\\Users\\Bevan\\Desktop\\New folder (3)\\myflaskapp\\flaskblog\\site.db')
            c = conn.cursor()
            if form.record1.data:
                file_name1 = record(5)
                print(file_name1)
                if (file_name1 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer01 = :answer01, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer01': file_name1, 'id': 1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record2.data:
                file_name2 = record(5)
                if (file_name2 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer02 = :answer02, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer02': file_name2, 'id': 1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record3.data:
                file_name3 = record(5)
                if (file_name3 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer03 = :answer03, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer03': file_name3, 'id': 1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record4.data:
                file_name4 = record(5)
                if (file_name4 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer04 = :answer04, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer04': file_name4, 'id': 1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record5.data:
                file_name5 = record(5)
                if (file_name5 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer05 = :answer05, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer05': file_name5, 'id': 1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            conn.close()
        elif(speaks[-1].user_id != current_user):
            speak = Speakinganswer(
                id=speaks[-1].id+1, pid=speaking_id, date_posted=datetime.now(), speakanswer=current_user)
            db.session.add(speak)
            db.session.commit()

            if form.record1.data:
                file_name1 = record(5)
                print(file_name1)
                if (file_name1 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer01 = :answer01, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer01': file_name1, 'id': speaks[-1].id+1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record2.data:
                file_name2 = record(5)
                if (file_name2 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer02 = :answer02, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer02': file_name2, 'id': speaks[-1].id+1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record3.data:
                file_name3 = record(5)
                if (file_name3 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer03 = :answer03, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer03': file_name3, 'id': speaks[-1].id+1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record4.data:
                file_name4 = record(5)
                if (file_name4 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer04 = :answer04, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer04': file_name4, 'id': speaks[-1].id+1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record5.data:
                file_name5 = record(5)
                if (file_name5 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer0 = :answer05, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer05': file_name5, 'id': speaks[-1].id+1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            conn.close()
        elif (datetime.now() - speaks[-1].date_posted > timedelta(seconds=900)) and (speaks[-1].user_id == current_user):
            print(speaks[-1].id)
            speak = Speakinganswer(
                id=speaks[-1].id+1, pid=speaking_id, date_posted=datetime.now(), speakanswer=current_user)
            db.session.add(speak)
            db.session.commit()
            conn = sqlite3.connect(
                'C:\\Users\\Bevan\\Desktop\\New folder (3)\\myflaskapp\\flaskblog\\site.db')
            c = conn.cursor()
            if form.record1.data:
                file_name1 = record(5)
                print(file_name1)
                if (file_name1 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer01 = :answer01, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer01': file_name1, 'id': speaks[-1].id+1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record2.data:
                file_name2 = record(5)
                if (file_name2 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer02 = :answer02, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer02': file_name2, 'id': speaks[-1].id+1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record3.data:
                file_name3 = record(5)
                if (file_name3 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer03 = :answer03, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer03': file_name3, 'id': speaks[-1].id+1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record4.data:
                file_name4 = record(5)
                if (file_name4 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer04 = :answer04, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer04': file_name4, 'id': speaks[-1].id+1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record5.data:
                file_name5 = record(5)
                if (file_name5 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer05 = :answer05, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer05': file_name5, 'id': speaks[-1].id+1, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            conn.close()

        elif (datetime.now() - speaks[-1].date_posted <= timedelta(seconds=900)) and (speaks[-1].user_id == current_user):
            conn = sqlite3.connect(
                'C:\\Users\\Bevan\\Desktop\\New folder (3)\\myflaskapp\\flaskblog\\site.db')
            c = conn.cursor()
            if form.record1.data:
                file_name1 = record(5)
                print(file_name1)
                if (file_name1 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer01 = :answer01, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer01': file_name1, 'id': speaks[-1].id, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record2.data:
                file_name2 = record(5)
                if (file_name2 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer02 = :answer02, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer02': file_name2, 'id': speaks[-1].id, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record3.data:
                file_name3 = record(5)
                if (file_name3 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer03 = :answer03, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer03': file_name3, 'id': speaks[-1].id, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record4.data:
                file_name4 = record(5)
                if (file_name4 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer04 = :answer04, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer04': file_name4, 'id': speaks[-1].id, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            elif form.record5.data:
                file_name5 = record(5)
                if (file_name5 != 'none'):
                    c.execute("""UPDATE Speakinganswer SET answer05 = :answer05, date_posted = :date_posted
                                WHERE id = :id AND qid = :qid AND pid = :pid AND user_id = :user_id """,
                              {'answer05': file_name5, 'id': speaks[-1].id, 'pid': speaking_id, 'user_id': current_user, 'date_posted': datetime.now()})
                    conn.commit()
            conn.close()
        speaks = Speakinganswer.query.all()
        return render_template('speaking_paper.html',  speaking=speaking, form=form, speaks=speaks)
    return render_template('speaking_paper.html',  speaking=speaking, form=form)
