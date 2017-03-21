# tokenlib-signup

Example using tokenlib signup with user token confirmation

This is a project as an example to run a user sign up process using the tokenlib package.

The sign up view gets the user data an makes a token, that is read by the confirm view. This token can be send by email, for example. The confirm view then reads the token and creates the user instance in the database. In this example a dictionary database was used.

A login and auth view were added just to test the registered user. A DB view was added too, to list all the DB keys.

## How to run:

1. `git clone https://github.com/fcgomes92/tokenlib-signup.git`

2. `cd tokenlib-signup`

3. `pip install -r requirements.txt`

4. `python main.py`

### If you want to use virtualenv, do the following before the item 2:

1. `virtualenv tokenlib-signup-virtualenv`

2. `source tokenlib-signup-virtualenv/bin/activate`

## Dependencies:

- Python==3.x
- Flask==0.12
- python-decouple==3.0
- tokenlib==0.3.1
- WTForms==2.1
