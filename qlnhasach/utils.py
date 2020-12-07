from qlnhasach.models import Sach, QuyDinh
from flask import request
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
