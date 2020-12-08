from flask_login import login_user, login_manager, logout_user
from flask import render_template, redirect, request, url_for
from qlnhasach import app, login
from qlnhasach.admin import *
from qlnhasach.models import User
import hashlib


@app.route('/')
def route_main():
    return render_template('login.html')


@app.route("/login", methods=['get', 'post'])
def route_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                                 User.password == password).first()

        if user:
            login_user(user=user)
            return redirect('/admin')

    # elif request.method == 'GET':
    #     print(request.url)
    # elif request.method == 'GET':
    #     print(request.url)


@app.route('/')
def route_logout():
    logout_user()
    return redirect(url_for('/login'))


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


@app.route('/user')
def home():
    dssach = utils.read_data()
    return render_template('client/home.html', dssach=dssach)


if __name__ == "__main__":
    app.run(debug=True, port=4000)