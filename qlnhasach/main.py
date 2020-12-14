import login as login
from flask_login import login_user, login_manager, login_required, current_user, logout_user
from flask import render_template, redirect, request, url_for, session, jsonify, copy_current_request_context
from qlnhasach import app, models, utils, login
from qlnhasach.admin import *
from qlnhasach.models import User, KhachHang, connect
import hashlib

@app.route("/login", methods=['get', 'post'])
def route_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = str(hashlib.md5(request.form.get("password").strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            login_user(user=user)
            return redirect('/admin')
        costumer = KhachHang.query.filter(KhachHang.username == '#KH_'+username, KhachHang.password == password).first()
        if costumer:
            login_user(costumer,remember=True)
            return redirect('/')
        else:
            return render_template('login.html', msg='Tài khoản hoặc mật khẩu không đúng, hãy thử lại')
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def route_register():
    if request.method == 'POST':
        name = request.form.get('re_name')
        username = request.form.get('re_username')
        password = request.form.get('re_password', '').strip()
        datetime_object = request.form.get('re_date', '').strip()
        location = request.form.get('re_location')
        phone = str(request.form.get('re_phone'))
        email = request.form.get('re_email')

        #KIểm tra trùng tên
        khach = KhachHang.query.filter_by(username=username).first()
        if khach:
            return render_template( 'register.html',
                                    msg='Tên tài khoản đã được sử dụng',
                                success=False)


        #Kiểm tra nếu số điện thoại đã được đăng kí
        khach = KhachHang.query.filter_by(dien_thoai=phone).first()
        if khach:
            return render_template('register.html',
                                   msg='Số điện thoại đã được đăng kí',
                                   success=False)

        if phone.isdigit():
            return render_template('register.html',
                                   msg='Số điện thoại không hợp lệ',
                                   success=False)
        khach = KhachHang.query.filter_by(email=email).first()
        if khach:
            return render_template('register.html',
                                   msg='Email đã được đăng kí',
                                   success=False)

        # tạo user
        if utils.add_costumer(name=name, username='#KH_'+username, diachi=location, ngaysinh=datetime_object,
                         dienthoai=phone, password=password, email=email):
            return redirect('/')
        return render_template( 'login.html',
                                msg='Đăng kí thành công, mời đăng nhập',
                           success=True)
    else:
        return render_template( 'register.html')


@app.route("/books/details/<int:book_id>")
def book_detail(book_id):
    book = utils.get_book_by_Id(book_id=book_id)
    return render_template('client/book_details.html', sach = book)


@app.route('/search/details/"')
def searchkw():
    kw = request.args.get("kw")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    dssach = utils.read_books(kw, from_price, to_price)
    return render_template('client/search.html',dssach)


@app.route('/api/cart', methods=['post'])
@login_required
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}

    data = request.json
    id = str(data.get('id'))
    ten_sach = data.get('ten_sach')
    don_gia = data.get('don_gia')

    cart = session['cart']
    if id in cart:
        quan = cart[id]['quantity']
        cart[id]['quantity'] = int(quan) + 1
    else:
        cart[id] = {
            "id": id,
            "ten_sach": ten_sach,
            "don_gia": don_gia,
            "quantity": 1
        }

    session['cart'] = cart
    quan, price = utils.cart_stats(session['cart'])

    return jsonify({
        'cart' : session['cart'],
        'total_quantity': quan,
        'total_amount': price
    })


@app.route('/cart-infor', methods=['get', 'post'])
@login_required
def cart():
    quan, price = utils.cart_stats(session.get('cart'))
    cart_info = {
        'total_quantity': quan,
        'total_amount': price
    }
    return render_template('client/cart.html', cart_info=cart_info)


@app.route('/payment-infor/')
@login_required
def checkout():
    quan, price = utils.cart_stats(session.get('cart'))
    return render_template("client/user-infor.html", quan = quan, price = price)


@app.route('/payment', methods=['get', 'post'])
@login_required
def payment():
    if request.method == 'POST':
        if utils.add_receipt(session.get('cart')):
            del session['cart']
            return render_template('client/home.html', msg='T')
        else:
            return render_template('client/home.html', msg='F')
    return render_template('client/user-infor.html')


@app.route('/logout')
@login_required
def route_logout():
    logout_user()
    return redirect('/')


@app.login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'),404


@app.errorhandler(403)
def not_found_error(error):
    return render_template('page-403.html'),403


@app.route('/')
def home():
    dssach = utils.read_data()
    return render_template('client/home.html', dssach=dssach)

@app.route('/search')
def search():
    return render_template('client/search.html')


@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)


@app.route('/chitiet', methods=['GET'])
@login_required
def nhapsach():
    idphieunhap= int (request.form.get['id_sachnhap'])
    soluongnhap = int(request.form.get['so_luong'])
    sach = utils.nhap_sach(idSachNhap=idphieunhap,soLuongNhap=soluongnhap)
    return redirect('/admin')


if __name__ == "__main__":
    app.run(debug=True, port=4000)