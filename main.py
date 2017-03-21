from flask import Flask, request, render_template, session, redirect

from decouple import config

import tokenlib

import users

import util

import auth

app = Flask(__name__)
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
    form = users.LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = auth.check_auth(
            form.email.data, util.set_password(form.password.data))
        if user:
            session['user'] = user.email
            session['user_auth'] = user.password
            return redirect('/user')
    return render_template('login.html', form=form)


@app.route('/logout')
@auth.requires_auth
def logout():
    del session['user']
    del session['user_auth']
    return redirect('/')


@app.route('/user')
@auth.requires_auth
def user():
    return render_template('user.html', user=session.get('user'))


@app.route('/confirm/<string:token>')
def confirm(token):
    try:
        data = token_manager.parse_token(token)
    except ValueError as e:
        return '{}'.format(e)
    user = users.User(**data)
    user, status = user.save()
    return redirect('/login') if status else "User already confirmed"


@app.route('/db')
def db():
    import pprint
    return pprint.pformat(users.usersDB.db.ids, indent=4)

if __name__ == '__main__':
    test_users = [
        {'email': 'test1@t.com', 'phone': '35 9 8861 7068',
            'password': 'qwe123', 'origin': 'origem 2', 'full_name': 'test test'},
        {'email': 'test2@t.com', 'phone': '35 9 8861 7068',
            'password': 'qwe123', 'origin': 'origem 2', 'full_name': 'test test'},
        {'email': 'test3@t.com', 'phone': '35 9 8861 7068',
            'password': 'qwe123', 'origin': 'origem 2', 'full_name': 'test test'},
        {'email': 'test4@t.com', 'phone': '35 9 8861 7068',
            'password': 'qwe123', 'origin': 'origem 2', 'full_name': 'test test'},
        {'email': 'test5@t.com', 'phone': '35 9 8861 7068',
            'password': 'qwe123', 'origin': 'origem 2', 'full_name': 'test test'},
    ]
    for u in test_users:
        users.User(**u).save()
    app.run()
