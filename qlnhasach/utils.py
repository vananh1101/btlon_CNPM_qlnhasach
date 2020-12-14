from sqlalchemy import func, and_

from qlnhasach.models import Sach, QuyDinh, ChiTietPhieuNhap, PhieuNhapSach, KhachHang, ChiTietHoaDon, HoaDon
import hashlib
from qlnhasach import db


def read_data():
    dssach = Sach.query
    return dssach.all()


def add_costumer(name, username, password, dienthoai, diachi, ngaysinh, email):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = KhachHang(ho_ten=name,
                  dia_chi=diachi,
                  username=username,
                  password=password,
                  dien_thoai=dienthoai,
                  ngay_sinh=ngaysinh,
                  email=email)
    try:
        db.session.add(u)
        db.session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False


def du_lieu_ten_sach():
    dsTenSach = read_data()
    tenSach = []
    if dsTenSach:
        for sach in dsTenSach:
            tenSach.append(sach.ten_sach)
    return tenSach


def doc_dsKH():
    dsKH = KhachHang.query
    return dsKH.all()


def du_lieu_ten_khach():
    dsKH = doc_dsKH()
    dsKhach = []
    if dsKH:
        for kh in dsKH:
            dsKhach.append(kh.ho_ten)
    return dsKhach


def du_lieu_sach_ton(thang):
    dsTenSach = du_lieu_ten_sach()
    tongNhap = []
    tonDau = []
    tonCuoi = []
    tongXuat = []

    dsNhap = db.session.query(Sach.ten_sach,func.sum(ChiTietPhieuNhap.so_luong)) \
        .join(PhieuNhapSach, PhieuNhapSach.id == ChiTietPhieuNhap.id_phieu) \
        .join(Sach, Sach.id == ChiTietPhieuNhap.id_sachnhap) \
        .filter(func.month(PhieuNhapSach.ngay_nhap) == thang).group_by(Sach.id).all()

    if dsNhap:

        for sach in dsNhap:
            tongNhap.append(int(sach[1]))

    dsXuat = db.session.query(func.sum(ChiTietHoaDon.so_luong_mua)) \
        .join(HoaDon, HoaDon.id == ChiTietHoaDon.id_hoadon) \
        .join(Sach, Sach.id == ChiTietHoaDon.id_sach) \
        .filter((func.month(HoaDon.ngay_nhap) == thang)) \
        .group_by(Sach.ten_sach).all()
    if dsXuat:
        for sach in dsXuat:
            tongXuat.append(int(sach[0]))
    for ten in dsTenSach:
        # dsNhap = db.session.query(Sach.ten_sach, func.sum(ChiTietPhieuNhap.so_luong)) \
        #     .join(PhieuNhapSach, PhieuNhapSach.id == ChiTietPhieuNhap.id_phieu) \
        #     .join(Sach, Sach.id == ChiTietPhieuNhap.id_sachnhap) \
        #     .filter(and_(func.month(PhieuNhapSach.ngay_nhap) == thang, Sach.ten_sach.like(ten))) \
        #     .value(func.sum(ChiTietPhieuNhap.so_luong))

        # dsXuat = db.session.query(func.sum(ChiTietHoaDon.so_luong_mua)) \
        #     .join(HoaDon, HoaDon.id == ChiTietHoaDon.id_hoadon).join(Sach, Sach.id == ChiTietHoaDon.id_sach) \
        #     .filter(and_(func.month(HoaDon.ngay_nhap) == thang, Sach.ten_sach.like(ten))) \
        #     .value(func.sum(ChiTietHoaDon.so_luong_mua))

        dsTonDau = db.session.query(Sach.ten_sach, ChiTietPhieuNhap.so_luong, Sach.so_luong) \
            .join(PhieuNhapSach, PhieuNhapSach.id == ChiTietPhieuNhap.id_phieu) \
            .join(Sach, Sach.id == ChiTietPhieuNhap.id_sachnhap) \
            .filter(and_(func.month(PhieuNhapSach.ngay_nhap) == thang, Sach.ten_sach.like(ten))) \
            .order_by(PhieuNhapSach.ngay_nhap).first()

        dsTonCuoi = db.session.query(Sach.ten_sach, ChiTietPhieuNhap.so_luong, Sach.so_luong) \
            .join(PhieuNhapSach, PhieuNhapSach.id == ChiTietPhieuNhap.id_phieu) \
            .join(Sach, Sach.id == ChiTietPhieuNhap.id_sachnhap) \
            .filter(and_(func.month(PhieuNhapSach.ngay_nhap) == thang, Sach.ten_sach.like(ten))) \
            .order_by(PhieuNhapSach.ngay_nhap.desc()).first()

        if dsTonDau:
            tonDau.append(dsTonDau[2])
        if dsTonCuoi:
            tonCuoi.append(dsTonCuoi[2])
        # if dsNhap:
        #     tongNhap.append(int(dsNhap))
        # if dsXuat:
        #     tongXuat.append(int(dsXuat))

    return tonDau, tonCuoi, tongNhap, tongXuat


def quy_dinh_nhap_sach():
    minNhap = QuyDinh.query.value(QuyDinh.so_luong_nhap_toi_thieu)
    maxSachTon = QuyDinh.query.value(QuyDinh.so_luong_ton_toi_thieu)
    return minNhap, maxSachTon


def du_lieu_kh_no(thang):
    dsKH = du_lieu_ten_khach()
    tongTra = []
    noDau = []
    noCuoi = []
    tongNo = []

    dsNo = db.session.query(func.sum(ChiTietHoaDon.don_gia)) \
        .join(HoaDon, HoaDon.id == ChiTietHoaDon.id_hoadon) \
        .join(KhachHang, KhachHang.id == HoaDon.id_khachhang) \
        .filter(func.month(HoaDon.ngay_nhap) == 9).group_by(KhachHang.id).all()

    for ten in dsKH:

        dsTra = db.session.query(func.sum(ChiTietHoaDon.so_luong_mua)) \
            .join(HoaDon, HoaDon.id == ChiTietHoaDon.id_hoadon).join(Sach, Sach.id == ChiTietHoaDon.id_sach) \
            .filter(and_(func.month(HoaDon.ngay_nhap) == thang, Sach.ten_sach.like(ten))) \
            .value(func.sum(ChiTietHoaDon.so_luong_mua))

        dsNoDau = db.session.query(Sach.ten_sach, ChiTietPhieuNhap.so_luong, Sach.so_luong) \
            .join(PhieuNhapSach, PhieuNhapSach.id == ChiTietPhieuNhap.id_phieu) \
            .join(Sach, Sach.id == ChiTietPhieuNhap.id_sachnhap) \
            .filter(and_(func.month(PhieuNhapSach.ngay_nhap) == thang, Sach.ten_sach.like(ten))) \
            .order_by(PhieuNhapSach.ngay_nhap).first()

        dsNoCuoi = db.session.query(Sach.ten_sach, ChiTietPhieuNhap.so_luong, Sach.so_luong) \
            .join(PhieuNhapSach, PhieuNhapSach.id == ChiTietPhieuNhap.id_phieu) \
            .join(Sach, Sach.id == ChiTietPhieuNhap.id_sachnhap) \
            .filter(and_(func.month(PhieuNhapSach.ngay_nhap) == thang, Sach.ten_sach.like(ten))) \
            .order_by(PhieuNhapSach.ngay_nhap.desc()).first()

        if dsNoDau:
            noDau.append(dsNoDau[2])
        if dsNoCuoi:
            noCuoi.append(dsNoCuoi[2])
        if dsTra:
            tongTra.append(int(dsTra))
        if dsNo:
            tongNo.append(int(dsNo))

    return noDau, noCuoi, tongTra, tongNo
