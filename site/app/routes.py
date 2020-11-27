from datetime import datetime
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
from app.forms import LoginForm, RegistrationForm, LabelForm

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
    return "label home"


@app.route('/label/<int:batch_id>/<int:instance>/<int:index>', methods=['GET', 'POST'])
@login_required
def label_path(batch_id, instance, index):
    if (instance >= constants.NUM_INSTANCES):
        return redirect(url_for('label_home'))

    # if index out of bounds, redirect to 0
    images = Image.query.filter_by(batch_id=batch_id).order_by(Image.id.asc()).all()
    # Note that index cannot be negative since it will not match as an int. Would have to handle negatives by myself
    if (index >= len(images) or index < 0):
        if (index == 0):
            # TODO: figure out what to do if batch is empty, probs just redirect to label and flash message
            return "Batch is empty"
        else:
            return redirect(url_for('label_path', batch_id=batch_id, instance=instance, index=0))

    # Get image of this index
    image = images[index]

    form = LabelForm()
    if form.validate_on_submit():
        label = Label.query.filter_by(user_id=current_user.id).filter_by(instance=instance).filter_by(image_id=image.id).first()
        print("Previous label: ", label)
        if (label is None):
            print("Creating new label")
            label = Label(user_id=current_user.id, image_id=image.id, instance=instance)
        label.side_user_clicked = form.sideChosen.data
        label.measurement = form.length.data
        label.timestamp = datetime.utcnow()
        db.session.add(label)
        db.session.commit()
        print("new label:", label)
        flash(f'Saved label for image {image.id} successfully')
        return redirect(url_for('label_path', batch_id=batch_id, instance=instance, index=index))

    queryLabels = Label.query.filter_by(user_id=current_user.id).filter_by(instance=instance).join(Image).filter_by(batch_id=batch_id).all()
    currentLabel = None
    labeledImageIds = set()
    for label in queryLabels:
        if (label.image_id == image.id):
            if (currentLabel is not None):
                print("Database error: multiple labels by same user for image, using last one")
            currentLabel = label
            # Update form so that it has the previously saved results
            form.length.default = currentLabel.measurement
            form.sideChosen.default = currentLabel.side_user_clicked
            form.process()
        labeledImageIds.add(label.image_id)

    return render_template('image-selection.html',  putCorrectLeft=bool(image.side_with_lesion == constants.LEFT),
                                                    index=index,
                                                    image=image,
                                                    currentLabel=currentLabel,
                                                    images=images,
                                                    labeledImageIds=labeledImageIds,
                                                    batch_id=batch_id,
                                                    form=form,
                                                    instance=instance)

# wl and ww should be between 0-100
@app.route("/imagedata/<int:image_id>/<int:wl>/<int:ww>/false.png", methods=['GET'])
def imagedata_false(image_id, wl, ww):
    image = Image.query.get(image_id)
    # TODO: Make more robust?
    if (image is None):
        return "Invalid image id"


    fig=Figure(figsize=(6.4, 6.4))
    ax=fig.add_subplot(111)

    image_filepath = image.getFakeFilePath()
    print("FILEPATH:", image_filepath)
    with app.open_resource(f'static\\{image_filepath}') as f:
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

@app.route("/imagedata/<int:image_id>/<int:wl>/<int:ww>/true.png", methods=['GET'])
def imagedata_true(image_id, wl, ww):
    image = Image.query.get(image_id)
    # TODO: Make more robust?
    if (image is None):
        return "Invalid image id"


    fig=Figure(figsize=(6.4, 6.4))
    ax=fig.add_subplot(111)

    image_filepath = image.getFilePath()
    print("FILEPATH:", image_filepath)
    with app.open_resource(f'static\\{image_filepath}') as f:
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
