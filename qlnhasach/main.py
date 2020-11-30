from flask_login import login_user, login_manager
from flask import render_template, redirect, request, url_for
from qlnhasach import app, login
from qlnhasach.admin import *
from qlnhasach.models import User
import hashlib


# @app.route('/login-admin', methods=["post", "get"])
# def login_admin():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = str(hashlib.md5(request.form.get("password").strip().encode("utf-8")).hexdigest())
#         user = User.query.filter(User.username == username.strip(),
#                                  User.password == password).first()
#         if user:
#             login_user(user=user)
#         return render_template('login.html')
#     return redirect("/admin")


@app.route('/')
def route_main():
    return render_template('login.html')


@app.route("/login", methods=['get', 'post'])
def route_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = str(hashlib.md5(request.form.get("password").strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username,
                                 User.password == password).first()

        if user:
            login_user(user=user)

    # elif request.method == 'GET':
    #     print(request.url)
    return redirect('/admin')


@app.route('/logout')
def route_logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/ketoan')
def route_ketoan():
    return render_template('ketoan/accountant_page.html')


@app.route('/thukho')
def route_accountant():
    return render_template('thukho/stocker_page.html')


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True, port=4000)
