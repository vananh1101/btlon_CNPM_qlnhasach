from qlnhasach.models import Sach, QuyDinh
from flask import request
import json, hashlib
from qlnhasach.models import KhachHang
from qlnhasach import db


def add_costumer(name, username, password, dienthoai, diachi, ngaysinh):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = KhachHang(name=name,
                  diachi=diachi,
             username=username,
             password=password,
             dienthoai=dienthoai,
                  ngaysinh=ngaysinh)
    try:
        db.session.add(u)
        db.session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False


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
    u = KhachHang(name=name,
                  diachi=diachi,
             username=username,
             password=password,
             dienthoai=dienthoai,
                  ngaysinh=ngaysinh)
    try:
        db.session.add(u)
        db.session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False