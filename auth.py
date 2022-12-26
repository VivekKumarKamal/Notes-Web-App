from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('login_password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged IN', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Password", category='error')
        else:
            flash('Email not found', category='error')

    data = request.form
    print(data)
    return render_template("login.html", user = current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':


        email = request.form.get('email')
        first_name = request.form.get('first-name')
        second_name = request.form.get('second-name')
        password1 = request.form.get('pswrd1')
        password2 = request.form.get('pswrd2')


        user = User.query.filter_by(email=email).first()
        if user:
            flash("This user already exists. Log in", category='error')
            redirect(url_for('auth.login'))

        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        # elif len(first_name) < 2:
        #     flash('first name cannot be short than 2 characters', category='error')
        elif password1 != password2:
            flash("Passwords don't match")
        elif len(password1) < 7:
            flash("Password is too short, should be greater than 7 characters")

        else:
            new_user = User(email = email, first_name = first_name, second_name = second_name, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash('Account Created!', category='success')
            login_user(new_user, remember=True)

            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)


@auth.route('/log-out')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
