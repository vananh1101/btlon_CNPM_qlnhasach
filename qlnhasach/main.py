from flask_login import login_user, login_manager, login_required, current_user
from flask import render_template, redirect, request, url_for, session
from qlnhasach import app, models, utils,login
from qlnhasach.admin import *
from qlnhasach.models import User, KhachHang
import hashlib


@app.route("/login", methods=['get', 'post'])
def route_login():
    if request.method == "POST":

        username = request.form.get("username")
        password = str(hashlib.md5(request.form.get("password").strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username, User.password == password).first()
        costumer = KhachHang.query.filter(KhachHang.username == '#KH_'+username, KhachHang.password == password).first()
        if user:
            login_user(user=user)
            return redirect('/admin')
        if costumer:
            login_user(user=costumer)
            return redirect('/home')
        else:
            return render_template('login.html', msg='Tài khoản hoặc mật khẩu không đúng, hãy thử lại')
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def route_register():
    if request.method == 'POST':
        name = request.form.get('re_name')
        username = request.form.get('re_username')
        password = request.form.get('re_password', '').strip()
        datetime_object = request.form.get('re_date','').strip()
        location = request.form.get('re_location')
        phone = str(request.form.get('re_phone'))


        #KIểm tra trùng tên
        khach = KhachHang.query.filter_by(username=username).first()
        if khach:
            return render_template( 'register.html',
                                    msg='Tên tài khoản đã được sử dụng',
                                success=False)


        #Kiểm tra nếu số điện thoại đã được đăng kí
        khach = KhachHang.query.filter_by(dienthoai=phone).first()
        if khach:
            return render_template('register.html',
                                   msg='Số điện thoại đã được đăng kí',
                                   success=False)

        if phone.isalpha():
            return render_template('register.html',
                                   msg='Số điện thoại không hợp lệ',
                                   success=False)

        # tạo user
        if utils.add_costumer(name=name, username='#KH_'+username, diachi=location, ngaysinh=datetime_object,
                         dienthoai=phone, password=password):
            return redirect('/')
        return render_template( 'login.html',
                                msg='User created please <a href="/login">login</a>',
                           success=True)
    else:
        return render_template( 'register.html')


@app.route('/home')
@login_required
def login_r():
    pass


@app.route('/logout')
@login_required
def route_logout():
    logout_user()
    return redirect('/login')


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


@app.login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'),404


@app.errorhandler(403)
def not_found_error(error):
    return render_template('page-403.html'),403


@app.route('/user')
@login_required
def home():
    dssach = utils.read_data()
    return render_template('client/home.html', dssach=dssach)


@app.route('/chitiet', methods=['GET'])
@login_required
def nhapsach():
    idphieunhap= int (request.form.get['id_sachnhap'])
    soluongnhap = int(request.form.get['so_luong'])
    sach = utils.nhap_sach(idSachNhap=idphieunhap,soLuongNhap=soluongnhap)
    return redirect('/admin')


if __name__ == "__main__":
    app.run(debug=True, port=4000)