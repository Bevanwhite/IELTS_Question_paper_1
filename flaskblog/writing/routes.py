from flask import render_template, Blueprint, flash, url_for, redirect, request, abort
from flask_login import login_user, login_required, current_user
from flaskblog import db
from flaskblog.models import Writingpaper, Writingpaperanswer
from flaskblog.writing.forms import WritingpaperForm, WritingUpdateForm, WritingpapertwoForm, WritingpaperoneForm
from flaskblog.writing.utils import paper_picture


writing = Blueprint('writing', __name__)


@writing.route("/writing")
def write():
    page = request.args.get('page', 1, type=int)
    writingpapers = Writingpaper.query.paginate(page=page, per_page=6)
    return render_template('writing.html', writingpapers=writingpapers)


@writing.route("/writing/new", methods=['GET', 'POST'])
@login_required
def new_writingpaper():
    form = WritingpaperForm()
    if form.validate_on_submit():
        if form.task01_img.data:
            task01_file = paper_picture(form.task01_img.data)
            writingpaper = Writingpaper(title=form.title.data, task01=form.task01.data, task01_img=task01_file,
                                        task02=form.task02.data, wcreator=current_user)
        else:
            writingpaper = Writingpaper(title=form.title.data, task01=form.task01.data, task01_img=form.task01_img.data,
                                        task02=form.task02.data, wcreator=current_user)
        db.session.add(writingpaper)
        db.session.commit()
        flash('Your Writing Paper has been Created!', 'success')
        return redirect(url_for('writing.write'))
    return render_template('create_writing.html', title='Writing Paper', form=form, legend='Writing Paper')


@writing.route("/writing/<int:writing_id>", methods=['GET', 'POST'])
def show_writing(writing_id):
    writingpaper = Writingpaper.query.get_or_404(writing_id)
    form1 = WritingpaperoneForm()
    if form1.validate_on_submit():
        writing = Writingpaperanswer(pid=writing_id, task=form1.task01_answer.data,
                                     type="type1", wcandidate=current_user)
        db.session.add(writing)
        db.session.commit()
        flash(
            'Your Question 01 Answer has been saved in the database successfully', 'success')
        return redirect(url_for('writing.show_writing', writing_id=writing_id))
    form2 = WritingpapertwoForm()
    if form2.validate_on_submit():
        writing = Writingpaperanswer(pid=writing_id, task=form2.task02_answer.data,
                                     type="type2", wcandidate=current_user)
        db.session.add(writing)
        db.session.commit()
        flash(
            'Your Question 02 Answer has been saved in the database successfully', 'success')
        return redirect(url_for('writing.show_writing', writing_id=writing_id))
    return render_template('writing_paper.html',  writingpaper=writingpaper, form1=form1, form2=form2)


@writing.route("/writing/<int:writing_id>/update", methods=['GET', 'POST'])
@login_required
def update_writing(writing_id):
    writing = Writingpaper.query.get_or_404(writing_id)
    if writing.wcreator != current_user:
        abort(403)
    form = WritingUpdateForm()
    if form.validate_on_submit():
        if form.task01_img.data:
            task01_file = paper_picture(form.task01_img.data)
            writing.task01_img = task01_file
        writing.title = form.title.data
        writing.task01 = form.task01.data
        writing.task02 = form.task02.data
        db.session.commit()
        flash('Your Writing Question Papers has been updated', 'success')
        return redirect(url_for('writing.show_writing', writing_id=writing.id))
    elif request.method == 'GET':
        form.title.data = writing.title
        form.task01.data = writing.task01
        form.task02.data = writing.task02
        form.task01_img.data = writing.task01_img
    return render_template('create_writing.html', title='Update', form=form, legend='Update')


@writing.route("/writing/<int:writing_id>/delete", methods=['POST'])
@login_required
def delete_writing(writing_id):
    writing = Writingpaper.query.get_or_404(writing_id)
    if writing.wcreator != current_user:
        abort(403)
    db.session.delete(writing)
    db.session.commit()
    flash('Your Writing Paper has been deleted!!', 'success')
    return redirect(url_for('writing.write'))


@writing.route("/writing/<int:writing_result_id>/result", methods=['POST', 'GET'])
@login_required
def result(writing_result_id):
    writing_answer = Writingpaperanswer.query.get_or_404(writing_result_id)
    if writing_answer.wcandidate != current_user:
        abort(403)
    else:
        return render_template('writing_answer.html', title='Update', legend='Update', writing_answer=writing_answer)
