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


class UserRole(UserEnum):
    ADMIN = 1
    Thu_kho = 2
    Thu_ngan = 3


# BẢNG USER
class User(QLBase, UserMixin):
    __tablename__ = 'user'

    ho_ten = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    avata = Column(String(100))
    user_role = Column(Enum(UserRole), nullable=False)


    # QUAN HỆ 1-N VỚI BẢNG PHIỂU THU TIỀN
    phieu_thu = relationship('PhieuThuTien', backref='user', lazy=True)

    # QUAN HỆ 1-N VỚI BẢNG PHIẾU NHẬP SÁCH
    phieu_nhap_sach = relationship('PhieuNhapSach', backref='user', lazy=True)

    def __str__(self):
        return self.ho_ten


# BẢNG KHÁCH HÀNG
class KhachHang(QLBase):
    __tablename__ = 'khach_hang'

    ho_ten = Column(String(100), nullable=False)
    ngay_sinh = Column(Date)
    dia_chi = Column(String(150))
    dien_thoai = Column(String(11))
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100))
    # QUAN HỆ 1-N VỚI BẢNG HOÁ ĐƠN
    hoa_don = relationship('HoaDon', backref='khach_hang', lazy=True)

    # QUAN HỆ 1-N VỚI BẢNG PHIỂU THU TIỀN
    phieu_thu_tien = relationship('PhieuThuTien', backref='khach_hang', lazy=True)


# BẢNG SÁCH
class Sach(QLBase):
    __tablename__ = 'sach'

    ten_sach = Column(String(250), nullable=False)
    tac_gia = Column(String(100), nullable=False)
    the_loai = Column(String(100), nullable=False)
    don_gia = Column(Float, nullable=False)
    so_luong = Column(Integer, nullable=False)
    hinh = Column(String(100))

    # QUAN HỆ 1-N VỚI BẢNG CHI TIẾT HOÁ ĐƠN
    chi_tiet_hoa_don = relationship('ChiTietHoaDon',
                                    backref='sach', lazy=True)

    # QUAN HỆ 1-N VỚI BẢNG CHI TIẾT PHIẾU NHẬP SÁCH
    chi_tiet_phieu_nhap = relationship('ChiTietPhieuNhap', backref='sach', lazy=True)

    def __str__(self):
        return self.ten_sach


# BẢNG HOÁ ĐƠN
class HoaDon(QLBase):
    __tablename__ = 'hoa_don'

    ngay_nhap = Column(Date, default=datetime.today())

    # KHOÁ NGOẠI BẢNG KHÁCH HÀNG( QUAN HỆ 1-N)
    id_khachhang = Column(Integer, ForeignKey('khach_hang.id'), nullable=False)

    # QUAN HỆ 1-N VỚI BẢNG CHI TIẾT HOÁ ĐƠN
    chi_tiet_hoa_don = relationship('ChiTietHoaDon',
                                    backref='hoa_don', lazy=True)


# BẢNG CHI TIẾT HOÁ ĐƠN
class ChiTietHoaDon(QLBase):
    __tablename__ = 'chi_tiet_hoa_don'

    so_luong_mua = Column(Integer, nullable=False)
    don_gia = Column(Float, nullable=False)
    # KHOÁ NGOẠI BẢNG HOÁ ĐƠN- SÁCH (1-N)
    id_sach = Column(Integer, ForeignKey('sach.id'), nullable=False)

    # KHOÁ NGOẠI BẢNG HOÁ ĐƠN (1-N)
    id_hoadon = Column(Integer, ForeignKey('hoa_don.id'), nullable=False)


# BẢNG LẬP PHIẾU THU TIỀN
class PhieuThuTien(QLBase):
    __tablename__ = 'phieu_thu_tien'

    ngay_thu_tien = Column(Date, nullable=False)
    tong_tien_thu = Column(Float, nullable=False)

    # KHOÁ NGOẠI VỚI BẢNG USER
    id_user = Column(Integer, ForeignKey('user.id'), nullable=False)

    # KHOÁ NGOẠI VỚI BẢNG KHÁCH HÀNG
    id_khachhang = Column(Integer, ForeignKey('khach_hang.id'), nullable=False)

    def __int__(self):
        return self.id


# BẢNG LẬP PHIẾU NHẬP SÁCH
class PhieuNhapSach(QLBase):
    __tablename__ = 'phieu_nhap_sach'

    ngay_nhap = Column(Date, default=datetime.now())
    # KHOÁ NGOẠI BẢNG USER( QUAN HỆ 1-N)
    id_thukho = Column(Integer, ForeignKey('user.id'), nullable=False)

    # QUAN HỆ 1-N VỚI BẢNG CHI TIẾT PHIẾU NHẬP SÁCH
    chi_tiet_phieu_nhap = relationship('ChiTietPhieuNhap', backref='phieu_nhap_sach', lazy=True)

    def __int__(self):
        return self.id


# BẢNG CHI TIẾT PHIẾU NHAP SACH
class ChiTietPhieuNhap(QLBase):
    __tablename__ = 'chi_tiet_nhap_phieu_sach'

    # KHOÁ NGOẠI VỚI BẢNG PHIẾU NHẬP SÁCH
    id_phieu = Column(Integer, ForeignKey('phieu_nhap_sach.id'), nullable=False)
    so_luong = Column(Integer, nullable=False)

    # KHOÁ NGOẠI VỚI BẢNG SÁCH
    id_sachnhap = Column(Integer, ForeignKey('sach.id'), nullable=False)

    def __int__(self):
        return self.id


class QuyDinh(QLBase):
    __tablename__ = 'quy_dinh'

    so_luong_nhap_toi_thieu = Column(Integer, nullable=False)
    so_luong_ton_toi_thieu = Column(Integer, nullable=False)
    tien_no_toi_da = Column(Float, nullable=False)
    so_luong_ton_sau_ban = Column(Integer, nullable=False)
    tien_thu_khong_vuot_tien_no = Column(Boolean, default=True, nullable=False)


if __name__ == "__main__":
    db.create_all()