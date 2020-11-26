from flask_login import login_user
from flask import render_template, redirect, request
from qlnhasach import app, login
from qlnhasach.admin import *
from qlnhasach.models import User
import hashlib


@app.route('/login-admin', methods=["post", "get"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = str(hashlib.md5(request.form.get("password").strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                                 User.password == password).first()
        if user:
            login_user(user=user)
    return redirect("/admin")


@app.route('/')
def route_default():
    return render_template('login.html')


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True, port=4000)