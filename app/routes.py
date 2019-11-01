from flask import render_template, flash, redirect, request, url_for, send_from_directory
from app import app, db
from app.forms import LoginForm, RegistrationForm, SizeForm
from app.models import User, Role
from werkzeug.urls import url_parse
from flask_login import logout_user, current_user, login_user, login_required
from flask_security import SQLAlchemyUserDatastore, roles_accepted
from werkzeug.utils import secure_filename
import math
import os
from functools import wraps
# import shopify
# from app.file_util import store_fileInfo


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            print(current_user)
            if current_user.isAdmin() is False:
                flash("That page requires admin access")
                return render_template('index.html')
            return f(*args, **kwargs)
        return wrapped
    return wrapper


@app.before_first_request
def before_first_request():
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')
    db.session.commit()



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
        if user.activated is False:
            flash('Please wait for login approval')
            return render_template('dog.html')
        login_user(user, remember=form.remember_me.data, force=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

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

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    phones = ["iphone", "android", "blackberry"]
    agent = request.headers.get('User-Agent')
    form = SizeForm()
    print(f"---------------------------------{agent}------------------------------------------")
    if any(phone in agent.lower() for phone in phones):
        if form.is_submitted():
            print(form.size.data)
            return redirect(f"http://semi-aquatics.myshopify.com/cart/{form.size.data}:1")
        return render_template('sorry.html', form =form)
    # for attr, value in vars(product).items():
    #     print(attr, value)
    # print(type(product))
    if form.is_submitted():
        print(form.size.data)
        # pass
        return redirect(f"http://semi-aquatics.myshopify.com/cart/{form.size.data}:1")
    return render_template('shirts.html', form = form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

