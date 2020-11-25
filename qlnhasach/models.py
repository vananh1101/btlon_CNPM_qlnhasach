from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Float, Column, Enum, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime
from qlnhasach import db


class QLBase(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class QLBaseV1(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

    def __str__(self):
        return self.name


# USER TABLE
class UserRole(UserEnum):
    ADMIN = 1
    Thu_kho = 2
    Thu_ngan = 3


class User(QLBase, UserMixin):
    __tablename__ = 'user'

    email = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    avatar = Column(String(100))
    joined_date = Column(Date, default=datetime.now())
    user_role = Column(Enum(UserRole), nullable=False)


# BẢNG KHÁCH HÀNG
class KhachHang(QLBase):
    __tablename__ = 'khachhang'

    ngaysinh = Column(Date)
    diachi = Column(String(150))
    dienthoai = Column(String(11))
    hoadon = relationship('HoaDon', backref='hoadon', lazy=True)


# BẢNG SÁCH
class Sach(QLBase):
    __tablename__ = 'sach'

    tacgia = Column(String(100), nullable=False)
    theloai = Column(String(100), nullable=False)
    dongia = Column(Float, nullable=False)
    soluong = Column(Integer, nullable=False)


# BẢNG HOÁ ĐƠN
class HoaDon(QLBaseV1):
    __tablename__ = 'hoadon'

    ngaynhap = Column(Date, default=datetime.now())

    # KHOÁ NGOẠI BẢNG KHÁCH HÀNG( QUAN HỆ 1-N)
    id_khachhang = Column(Integer, ForeignKey('khachhang.id'), nullable=False)

    # KHOÁ NGOẠI BẢNG SÁCH( QUAN HỆ N-N)
    chitiet = relationship('Sach', secondary='hoadon', lazy='subquery',
                           backref=backref('id', lazy=True))


# THIẾT LẬP QUAN HỆ MANY-TO-MANY BẢNG HOÁ ĐƠN - SÁCH
chi_tiet = db.Table('chitiethoadon',
                    Column('id_sach', Integer,
                           ForeignKey('sach.id'), primary_key=True),
                    Column('id_hoadon', Integer,
                           ForeignKey('hoadon.id'), primary_key=True),
                    Column('soluong', Integer, nullable=False),
                    Column('dongia', Float, nullable=False))


# BẢNG LẬP PHIẾU NHẬP SÁCH
class PhieuNhapSach(QLBaseV1):
    __tablename__ = 'phieunhapsach'

    ngay_nhap = Column(Date, default=datetime.now())

    # KHOÁ NGOẠI BẢNG KHÁCH HÀNG( QUAN HỆ 1-N)
    id_thukho = Column(Integer, ForeignKey('id'), nullable=False)

    # KHOÁ NGOẠI BẢNG SÁCH( QUAN HỆ N-N)

    



if __name__ == "__main__":
    db.create_all()
