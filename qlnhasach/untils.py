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