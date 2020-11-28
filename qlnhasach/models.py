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


class UserRole(UserEnum):
    ADMIN = 1
    Thu_kho = 2
    Thu_ngan = 3


# BẢNG USER
class User(QLBase, UserMixin):
    __tablename__ = 'user'

    email = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    avatar = Column(String(100))
    joined_date = Column(Date, default=datetime.now())
    user_role = Column(Enum(UserRole), nullable=False)

    # QUAN HỆ 1-N VỚI BẢNG PHIỂU THU TIỀN
    phieu_thu = relationship('PhieuThuTien', backref='user', lazy=True)

    # QUAN HỆ 1-N VỚI BẢNG PHIẾU NHẬP SÁCH
    phieu_nhap_sach = relationship('PhieuNhapSach', backref='user', lazy=True)


# BẢNG KHÁCH HÀNG
class KhachHang(QLBase):
    __tablename__ = 'khachhang'

    ngaysinh = Column(Date)
    diachi = Column(String(150))
    dienthoai = Column(String(11))

    # QUAN HỆ 1-N VỚI BẢNG HOÁ ĐƠN
    hoadon = relationship('HoaDon', backref='khachhang', lazy=True)

    # QUAN HỆ 1-N VỚI BẢNG PHIỂU THU TIỀN
    phieu_thu_tien = relationship('PhieuThuTien', backref='khachhang', lazy=True)


# BẢNG SÁCH
class Sach(QLBase):
    __tablename__ = 'sach'

    tacgia = Column(String(100), nullable=False)
    theloai = Column(String(100), nullable=False)
    dongia = Column(Float, nullable=False)
    soluong = Column(Integer, nullable=False)

    # QUAN HỆ 1-N VỚI BẢNG CHI TIẾT HOÁ ĐƠN
    chi_tiet_hoa_don = relationship('ChiTietHoaDon',
                                    backref='sach', lazy=True)

    # QUAN HỆ 1-N VỚI BẢNG CHI TIẾT PHIẾU NHẬP SÁCH
    chi_tiet_phieu_nhap = relationship('ChiTietPhieuNhap', backref='sach', lazy=True)


# BẢNG HOÁ ĐƠN
class HoaDon(QLBaseV1):
    __tablename__ = 'hoadon'

    ngaynhap = Column(Date, default=datetime.now())

    # KHOÁ NGOẠI BẢNG KHÁCH HÀNG( QUAN HỆ 1-N)
    id_khachhang = Column(Integer, ForeignKey('khachhang.id'), nullable=False)

    # QUAN HỆ 1-N VỚI BẢNG CHI TIẾT HOÁ ĐƠN
    chi_tiet = relationship('ChiTietHoaDon',
                            backref='hoadon', lazy=True)


# BẢNG CHI TIẾT HOÁ ĐƠN
class ChiTietHoaDon(QLBaseV1):
    __tablename__ = 'chitiethoadon'

    soluongmua = Column(Integer, nullable=False)
    dongia = Column(Float, nullable=False)
    # KHOÁ NGOẠI BẢNG HOÁ ĐƠN- SÁCH (1-N)
    id_sach = Column(Integer, ForeignKey('sach.id'), nullable=False)

    # KHOÁ NGOẠI BẢNG HOÁ ĐƠN (1-N)
    id_hoadon = Column(Integer, ForeignKey('hoadon.id'), nullable=False)


# BẢNG LẬP PHIẾU NHẬP SÁCH
class PhieuNhapSach(QLBaseV1):
    __tablename__ = 'phieunhapsach'

    ngay_nhap = Column(Date, default=datetime.now())

    # KHOÁ NGOẠI BẢNG USER( QUAN HỆ 1-N)
    id_thukho = Column(Integer, ForeignKey('user.id'), nullable=False)

    # QUAN HỆ 1-N VỚI BẢNG CHI TIẾT PHIẾU NHẬP SÁCH
    chi_tiet_nhap = relationship('ChiTietPhieuNhap',backref='phieunhapsach', lazy=True)


# BẢNG LẬP PHIẾU THU TIỀN
class PhieuThuTien(QLBaseV1):
    __tablename__ = 'phieuthutien'

    ngaythutien = Column(Date, nullable=False)
    tongtienthu = Column(Float, nullable=False)

    # KHOÁ NGOẠI VỚI BẢNG USER
    id_user = Column(Integer, ForeignKey('user.id'), nullable=False)

    # KHOÁ NGOẠI VỚI BẢNG KHÁCH HÀNG
    id_khachhang = Column(Integer, ForeignKey('khachhang.id'), nullable=False)


# BẢNG CHI TIẾT PHIẾU THU TIỀN
class ChiTietPhieuNhap(QLBaseV1):
    __tablename__ = 'chitietnhapphíeusach'

    soluongnhap = Column(Integer, nullable=False)

    # KHOÁ NGOẠI VỚI BẢNG PHIẾU NHẬP SÁCH
    id_phieu = Column(Integer, ForeignKey('phieunhapsach.id'), nullable=False)

    # KHOÁ NGOẠI VỚI BẢNG SÁCH
    id_sachnhap = Column(Integer, ForeignKey('sach.id'), nullable=False)


if __name__ == "__main__":
    db.create_all()
