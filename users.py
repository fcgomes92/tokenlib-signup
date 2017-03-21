from wtforms import (Form, StringField, PasswordField,
                     validators, ValidationError)

from pprint import PrettyPrinter

import util

pp = PrettyPrinter()


class User(object):

    def __init__(self, email, password, phone, origin, full_name, *args,
                 **kwargs):
        self.email = email
        self.phone = phone
        self.origin = origin
        self.full_name = full_name
        self.password = util.set_password(password=password)

    def save(self):
        return usersDB.add(self)

    def get(self, email):
        return usersDB.get(email)

    def __str__(self):
        return "{} - {}".format(self.email, self.full_name)


class DB(object):
    by_id = {}
    ids = []

    def __str__(self):
        pp.pprint(self.by_id)
        return ""


class UserDatabase(object):
    db = None

    def __init__(self):
        if not UserDatabase.db:
            UserDatabase.db = DB()

    def add(self, user: User):
        if user.email not in self.db.ids:
            self.db.by_id[user.email] = user
            self.db.ids.append(user.email)
            print('Adding user: {}'.format(user.email))
            return user, True
        else:
            return "User already in DB", False

    def get(self, email):
        return self.db.by_id.get(email)

usersDB = UserDatabase()


class RegistrationForm(Form):

    def validate_email(form, field):
        if usersDB.get(field.data):
            raise ValidationError("User already registered")

    email = StringField('Email', [validators.Length(min=6, max=35), ])
    phone = StringField('Phone', [validators.Length(min=6, max=35), ])
    origin = StringField('Origin', [validators.Length(min=6, max=35), ])
    full_name = StringField('Full Name', [validators.Length(min=6, max=35), ])
    password = PasswordField('Password', [validators.DataRequired(), ])


class LoginForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=35), ])
    password = PasswordField('Password', [validators.DataRequired(), ])
