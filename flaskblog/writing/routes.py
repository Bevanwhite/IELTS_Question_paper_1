from flask import render_template, Blueprint, flash, url_for, redirect
from flask_login import login_user, login_required, current_user
from flaskblog import db
from flaskblog.models import Writingpaper, Writingpaperanswer
from flaskblog.writing.forms import Writingpaper, WritingpaperanswerForm, WritingpaperForm
from flaskblog.writing.utils import paper_picture

writing = Blueprint('writing', __name__)


@writing.route("/writing")
def write():
    writingpapers = Writingpaper.query.all()
    return render_template('writing.html', writingpapers=writingpapers)


@writing.route("/writing/new", methods=['GET', 'POST'])
@login_required
def new_writingpaper():
    form = WritingpaperForm()
    if form.validate_on_submit():
        if form.task01_img.data and form.task02_img.data:
            task01_file = paper_picture(form.task01_img.data)
            task02_file = paper_picture(form.task02_img.data)
            writingpaper = Writingpaper(title=form.title.data, task01=form.task01.data, task01_img=task01_file,
                                        task02=form.task02.data, task02_img=task02_file, wcreator=current_user)
        elif form.task01_img.data:
            task01_file = paper_picture(form.task01_img.data)
            writingpaper = Writingpaper(title=form.title.data, task01=form.task01.data, task01_img=task01_file,
                                        task02=form.task02.data, task02_img=form.task02_img.data, wcreator=current_user)
        elif form.task02_img.data:
            task02_file = paper_picture(form.task02_img.data)
            writingpaper = Writingpaper(title=form.title.data, task01=form.task01.data, task01_img=form.task02.data,
                                        task02=form.task02.data, task02_img=task02_file, wcreator=current_user)
        else:
            writingpaper = Writingpaper(title=form.title.data, task01=form.task01.data, task01_img=form.task01.data,
                                        task02=form.task02.data, task02_img=form.task02_img.data, wcreator=current_user)
        db.session.add(writingpaper)
        db.session.commit()
        flash('Your Writing Paper has been Created!', 'success')
        return redirect(url_for('writing.write'))
    return render_template('create_writing.html', title='Writing Paper', form=form, legend='Writing Paper')


@writing.route("/writing/<int:writing_id>")
def show_writing(writing_id):
    form = WritingpaperanswerForm()
    writingpaper = Writingpaper.query.get_or_404(writing_id)

    return render_template('writing_paper.html', title=writingpaper.title, writingpaper=writingpaper, form=form)
