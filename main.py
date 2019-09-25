from flask import Flask, request, redirect, render_template
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template('login_form.html', title="Signup")    

def test_len(field):
    if len(field)>=3 and len(field)<=20:
        return True
    else:
        return False

def test_space(field):
    if ' ' not in field:
        return True
    else:
        return False
 
def validate_field(field):
    if test_len(field) and test_space(field):
        return True
    else:
        return False

@app.route('/', methods=['POST'])
def validate_signup():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    password_match_error = ''
    email_error = ''

    if not validate_field(username):
        username_error = 'That\'s not a valid username'

    if not validate_field(password):
        password_error = 'That\'s not a valid password'

    if not validate_field(verify_password) or password != verify_password:
        password_match_error = 'Passwords don\'t match'
    
    if email:
        if not validate_field(email) or email.count('.') != 1 or email.count('@') != 1:
            email_error = 'That\'s not a valid email'
    
    if not username_error and not password_error and not password_match_error and not email_error:
        return redirect('/welcome?username={0}'.format(username))
    else:
        return render_template('login_form.html', username=username, email=email, username_error=username_error, password_error=password_error, password_match_error=password_match_error, email_error=email_error)

@app.route('/welcome')
def valid_login():
    username = request.args.get('username')
    return render_template('welcome.html', title="Welcome", username=username)

app.run()