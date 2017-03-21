from flask import Flask, request, render_template, session, redirect

from decouple import config

import tokenlib

import users

import util

import auth

app = Flask(__name__)

# using decouple to get the configuration from .env
app.config.update(dict(
    DEBUG=config('DEBUG', False),
    SECRET_KEY=config('SECRET_KEY'),
    EMAIL_HOST=config('EMAIL_HOST', ''),
    EMAIL_PORT=config('EMAIL_PORT', ''),
    EMAIL_HOST_PASSWORD=config('EMAIL_HOST_PASSWORD', ''),
    EMAIL_HOST_USER=config('EMAIL_HOST_USER', ''),
    EMAIL_USE_SSL=config('EMAIL_USE_SSL', ''),
    TOKEN_MANAGER=tokenlib.TokenManager(
        secret=config('SECRET_KEY'),
        timeout=24 * 3600,
    )
))

token_manager = app.config.get('TOKEN_MANAGER')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST', ])
def signup():
    """
    This view tries to create a token based on the RegistrationForm
    The user is not created yet
    """
    # this form checks if a user with the same email exists
    form = users.RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        token = token_manager.make_token(dict(email=form.email.data,
                                              phone=form.phone.data,
                                              password=form.password.data,
                                              origin=form.origin.data,
                                              full_name=form.full_name.data,))
        return render_template('token.html', token=token)
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST', ])
def login():
    """
    This view authenticates the user based on the LoginForm
    """
    form = users.LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # if the authentication is valid the user instance is returned
        user = auth.check_auth(
            form.email.data, util.set_password(form.password.data))
        if user:
            # register the user authentication data in the session
            # so we can retrieve later during the requires_auth
            session['user'] = user.email
            session['user_auth'] = user.password
            return redirect('/user')
    return render_template('login.html', form=form)


@app.route('/logout')
@auth.requires_auth
def logout():
    """
    Removes the user data from session
    """
    del session['user']
    del session['user_auth']
    return redirect('/')


@app.route('/user')
@auth.requires_auth
def user():
    """
    This view renders the user email if authenticated
    """
    return render_template('user.html', user=session.get('user'))


@app.route('/confirm/<string:token>')
def confirm(token):
    """
    This view takes a token and
    checks if the data inside it is a new user or not
    Here the user instance is created and saved to the DB
    """
    try:
        data = token_manager.parse_token(token)
    except ValueError as e:
        return '{}'.format(e)

    # using the data an user instance is created
    user = users.User(**data)

    # and saved to the DB
    # the status indicates if the user was already created
    user, status = user.save()
    return redirect('/login') if status else "User already confirmed"


@app.route('/db')
def db():
    """
    This view renders a list of all the ids already in the DB
    """
    import pprint
    return pprint.pformat(users.usersDB.db.ids, indent=4)

if __name__ == '__main__':
    app.run()
