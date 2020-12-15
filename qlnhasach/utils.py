from qlnhasach.models import Sach, QuyDinh, HoaDon, ChiTietHoaDon
import hashlib
from qlnhasach.models import KhachHang
from qlnhasach import db
from flask_login import current_user
import sqlite3


def read_data():
    dssach = Sach.query
    return dssach.all()


def nhap_sach(soLuongNhap, idSachNhap):
    minNhap = QuyDinh.query.value(QuyDinh.so_luong_nhap_toi_thieu)
    maxSachTon = QuyDinh.query.value(QuyDinh.so_luong_ton_toi_thieu)
    soLuongTon = db.session.query(Sach.so_luong).filter(Sach.id == idSachNhap).value(Sach.so_luong)
    update = Sach.query.filter(Sach.id == idSachNhap).first()
    try:
        if soLuongNhap >= minNhap and soLuongTon < maxSachTon:
            update.so_luong += soLuongNhap
            db.session.commit()
    except Exception as ex:
        print(ex)


def add_costumer(name, username, password, dienthoai, diachi, ngaysinh, email):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = KhachHang(ho_ten=name,
                  dia_chi=diachi,
             username=username,
             password=password,
             dien_thoai=dienthoai,
                  ngay_sinh=ngaysinh,
                  email= email)
    try:
        db.session.add(u)
        db.session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False


def cart_stats(cart):
    if cart is None:
        return 0, 0

    books = cart.values()

    quantity = sum([b['quantity'] for b in books])
    price = sum([b['don_gia']*b['quantity'] for b in books])

    return quantity, price


def read_books(kw=None, from_price=None, to_price=None):
    books = Sach.query
    if kw:
        books = books.filter(Sach.ten_sach.contains(kw))

    if from_price and to_price:
        books = books.filter(Sach.don_gia.__gt__(from_price),
                                   Sach.don_gia.__lt__(to_price))
    return books.all()


def get_book_by_Id(book_id):
    return Sach.query.get(book_id)


def add_receipt(cart):
    if cart:
        try:
            receipt = HoaDon(id_khachhang=current_user.id)
            db.session.add(receipt)

            for p in list(cart.values()):
                detail = ChiTietHoaDon(id=int(p["id"]),
                                       id_hoadon=receipt.id,
                                       don_gia=float(p["don_gia"]),
                                       so_luong_mua=p["quantity"])
                db.session.add(detail)
            db.session.commit()

            return True
        except :
            pass

    return False


def check_login(username, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    return KhachHang.query.filter(KhachHang.username == username,
                                  KhachHang.password == password).first()
