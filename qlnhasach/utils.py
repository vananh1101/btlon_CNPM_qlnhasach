from qlnhasach.models import Sach, QuyDinh
import json, hashlib
from qlnhasach.models import KhachHang
from qlnhasach import db


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


def add_costumer(name, username, password, dienthoai, diachi, ngaysinh):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = KhachHang(ho_ten=name,
                  dia_chi=diachi,
             username=username,
             password=password,
             dien_thoai=dienthoai,
                  ngay_sinh=ngaysinh)
    try:
        db.session.add(u)
        db.session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False