from flask_login import login_user, login_manager
from flask import render_template, redirect, request, url_for
from qlnhasach import app, login, models
from qlnhasach.admin import *
from qlnhasach.models import User
import hashlib, os
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
            return redirect('/admin')
        return render_template('login.html', msg='Tài khoản hoặc mật khẩu không đúng, hãy thử lại')
    return redirect('/admin')
    # elif request.method == 'GET':
    #     print(request.url)


@app.route('/register', methods=['GET', 'POST'])
def route_register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        #KIểm tra trùng tên
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'register.html',
                                    msg='Tên tài khoản đã được sử dụng',
                                    success=False)

        # kiểm tra trùng
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'register.html',
                                    msg='Email đã được sử dụng',
                                    success=False)
        #kiểm tra rỗng
        if name =='':
            return render_template('register.html',
                                   msg='Tên không được rỗng',
                                   success=False)
        # kiểm tra cú pháp email


        # tạo user
        avatar = request.files["avatar"]
        avatar_path = 'images/upload/%s' % avatar.filename
        avatar.save(os.path.join(app.config['ROOT_PROJECT_PATH'],
                                 'static/', avatar_path))

        if models.add_user(name=name, email=email, username=username,
                          password=password, avatar=avatar_path):
            return redirect('/admin')

        return render_template( 'accounts/register.html',
                                msg='User created please <a href="/login">login</a>',
                           success=True)

    else:
        return render_template( 'register.html')


@app.route('/logout')
def route_logout():
    logout_user()
    return redirect(url_for('login'))


# @app.route('/ketoan')
# def route_ketoan():
#     return render_template('ketoan/accountant_page.html')
#
#
@app.route('/thukho')
def route_accountant():
    return render_template('thukho/stocker_page.html')


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True, port=4000)