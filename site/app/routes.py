import datetime
import random

import matplotlib.pyplot as plt
import pickle as pl

from app import constants

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

from io import BytesIO

from flask import render_template, flash, redirect, make_response, url_for, request

from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Label, Image, Batch

from app import app, db
from app.forms import LoginForm, RegistrationForm

from werkzeug.urls import url_parse


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    # TODO: if there is a next_page and they mess up logging in first time, make sure they redirect later maybe?
    # It might be that they always get redirected to home anyway
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
@login_required
def index():
    labels = [
        {
            'labeler': {'username': 'Yeet'},
            'timestamp': '4:20'
        },
        {
            'labeler': {'username': 'Yeet2'},
            'timestamp': '4:22'
        }
    ]
    return render_template('index.html', labels=labels)

@app.route('/database', methods=['GET'])
def display_tables():
    users = User.query.all()
    labels = Label.query.all()
    images = Image.query.all()
    batches = Batch.query.all()
    print(batches)
    return render_template('tables.html', users=users, labels=labels, images=images, batches=batches)

# TODO: figure out link id to redirect to (will also be able to show if it's been completed o rnot)
@app.route('/label', methods=['GET'])
def label_home():
    return render_template('image-selection.html', trueFirst=bool(random.getrandbits(1)), yeet=120)


@app.route('/label/<int:batch_id>/<int:index>')
@login_required
def label_path(batch_id, index):
    # if index out of bounds, redirect to 0
    images = Image.query.filter_by(batch_id=batch_id).order_by(Image.id.asc()).all()
    if (index >= len(images) or index < 0):
        if (index == 0):
            # TODO: figure out what to do if batch is empty, probs just redirect to label and flash message
            return "Batch is empty"
        else:
            return redirect(url_for(f'/label/{batch_id}/0'))

    queryLabels = Label.query.filter_by(user_id=current_user.id).filter_by(batch_id=batch_id).join(Image).all()
    labeledImageIds = set()
    for label in queryLabels:
        labeledImageIds.add(label.image_id)

    print(current_user)
    return render_template('image-selection.html', trueFirst=bool(random.getrandbits(1)))

# wl and ww should be between 0-100
@app.route("/imagedata/<int:image_id>/<int:wl>/<int:ww>/false.png")
def imagedata_false(image_id, wl, ww):
    fig=Figure(figsize=(6.4, 6.4))
    ax=fig.add_subplot(111)
    with app.open_resource('static\\images\\1\\test.pickle') as f:
        fig_handle = pl.load(f)
        vcenter = wl * 255 / 100
        vmin = int(vcenter - ww * 255 / 100 / 2)
        vmax = int(vcenter + ww * 255 / 100 / 2)
        print(vmin, vmax)
        ax.imshow(fig_handle, cmap='gray', vmin=max(0, vmin), vmax=min(255, vmax))

    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/imagedata/<int:image_id>/<int:wl>/<int:ww>/true.png")
def imagedata_true(image_id, wl, ww):
    fig=Figure(figsize=(6.4, 6.4))
    ax=fig.add_subplot(111)
    with app.open_resource('static\\images\\1\\test.pickle') as f:
        fig_handle = pl.load(f)
        vcenter = wl * 255 / 100
        vmin = int(vcenter - ww * 255 / 100 / 2)
        vmax = int(vcenter + ww * 255 / 100 / 2)
        print(vmin, vmax)
        ax.imshow(fig_handle, cmap='gray', vmin=max(0, vmin), vmax=min(255, vmax))

    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
