from flask_login import login_user, login_manager
from flask import render_template, redirect, request, url_for
from qlnhasach import app, login, models, untils
from qlnhasach.admin import *
from qlnhasach.models import User, KhachHang
import hashlib, os
from qlnhasach.untils import add_costumer
from datetime import datetime
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
        name = request.form.get('re_name')
        username = request.form.get('re_username')
        password = request.form.get('re_password', '').strip()
        confirm_password = request.form.get('re_confirm_password')
        datetime_object = request.form.get('re_date','').strip()
        location = request.form.get('re_location')
        phone = str(request.form.get('re_phone'))


        #KIểm tra trùng tên
        Khach = KhachHang.query.filter_by(username=username).first()
        if Khach:
            return render_template( 'register.html',
                                    msg='Tên tài khoản đã được sử dụng',
                                success=False)


        #Kiểm tra nếu số điện thoại đã được đăng kí
        Khach = KhachHang.query.filter_by(dienthoai=phone).first()
        if Khach:
            return render_template('register.html',
                                   msg='Số điện thoại đã được đăng kí',
                                   success=False)


        #kiểm tra rỗng
        if name =='':
            return render_template('register.html',
                                   msg='Tên không được trống',
                                   success=False)
        if username=='':
            return render_template('register.html',
                                   msg='Tên đăng nhập khônd được trống',
                                   success=False)
        if password=='':
            return render_template('register.html',
                                   msg='Mật khẩu không được trống',
                                   success=False)
        if phone=='':
            return render_template('register.html',
                                   msg='Số điện thoại không được trống',
                                   success=False)
        if location=='':
            return render_template('register.html',
                                   msg='Địa chỉ không được trống',
                                   success=False)
        if datetime_object=='':
            return render_template('register.html',
                                   msg='Ngày sinh không được trống',
                                   success=False)
        #kiểm tra nếu 2 pass word không trùng nhau
        if password != confirm_password:
            return render_template('register.html',
                                   msg='Xác nhận mật khẩu sai, hãy thử lại',
                                   success=False)
        # tạo user
        if untils.add_costumer(name=name, username=username, diachi=location, ngaysinh=datetime_object,
                         dienthoai=phone, password=password):
            return redirect('/admin')
        return render_template( 'register.html',
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