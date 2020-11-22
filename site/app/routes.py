import datetime
import random

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

from io import BytesIO

from flask import render_template, flash, redirect, make_response, url_for, request

from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

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
        return redirect(url_for('index'))
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
    print(users)
    return render_template('tables.html', users=users)


@app.route('/label', methods=['GET'])
def label_page():
    return render_template('image-selection.html', trueFirst=bool(random.getrandbits(1)), yeet=3)


@app.route("/imagedata/<int:amount>/false.png")
def imagedata_false(amount):
    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(amount):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-', color="red")
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/imagedata/true.png")
def imagedata_true():
    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-', color="green")
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
