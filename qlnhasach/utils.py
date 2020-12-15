from sqlalchemy import func, and_

from qlnhasach.models import Sach, QuyDinh, ChiTietPhieuNhap, PhieuNhapSach, KhachHang, ChiTietHoaDon, HoaDon, \
    PhieuThuTien
import hashlib
from qlnhasach import db


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


def du_lieu_sach():
    dsTenSach = db.session.query(Sach.id, Sach.ten_sach).all()
    tenSach = []
    if dsTenSach:
        for sach in dsTenSach:
            tenSach.append(sach.ten_sach)
    return tenSach


def du_lieu_khach_hang():
    dsKH = db.session.query(KhachHang.username,KhachHang.id).all()
    dsKhach = []
    if dsKH:
        for kh in dsKH:
            dsKhach.append(kh.username)
    return dsKhach


def du_lieu_sach_ton(thang):
    dsTenSach = du_lieu_sach()
    tongNhap = []
    tonDau = []
    tonCuoi = []
    tongXuat = []

    dsNhap = db.session.query(Sach.ten_sach, func.sum(ChiTietPhieuNhap.so_luong)) \
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

    for sach in dsTenSach:
        dsTon = db.session.query(ChiTietPhieuNhap.so_luong, Sach.so_luong) \
            .join(PhieuNhapSach, PhieuNhapSach.id == ChiTietPhieuNhap.id_phieu) \
            .join(Sach, Sach.id == ChiTietPhieuNhap.id_sachnhap) \
            .filter(and_(func.month(PhieuNhapSach.ngay_nhap) == thang, Sach.ten_sach.like(sach))) \
            .order_by(PhieuNhapSach.ngay_nhap).all()

        if dsTon:
            tonDau.append(dsTon[0][1])
            tonCuoi.append(dsTon[len(dsTon) - 1][1])

    return tonDau, tonCuoi, tongNhap, tongXuat


def du_lieu_kh_no(thang):
    dsKH = du_lieu_khach_hang()
    tongTra = []
    noDau = []
    noCuoi = []
    tongNo = []

    dsNo = db.session.query(func.sum(ChiTietHoaDon.don_gia)) \
        .join(HoaDon, HoaDon.id == ChiTietHoaDon.id_hoadon) \
        .join(KhachHang, KhachHang.id == HoaDon.id_khachhang) \
        .filter(func.month(HoaDon.ngay_nhap) == thang).group_by(KhachHang.id).all()
    if dsNo:
        for kh in dsNo:
            tongNo.append(float(kh[0]))

    dsTra = db.session.query(func.sum(PhieuThuTien.tong_tien_thu)) \
        .join(KhachHang, KhachHang.id == PhieuThuTien.id_khachhang) \
        .filter(func.month(PhieuThuTien.ngay_thu_tien) == thang).group_by(KhachHang.id).all()
    if dsTra:
        for kh in dsTra:
            tongTra.append(float(kh[0]))

    for kh in dsKH:
        # import pdb
        # pdb.set_trace()
        dsNo = db.session.query(ChiTietHoaDon.don_gia,ChiTietHoaDon.so_luong_mua) \
            .join(HoaDon, HoaDon.id == ChiTietHoaDon.id_hoadon) \
            .join(KhachHang, KhachHang.id == HoaDon.id_khachhang) \
            .filter(and_(func.month(HoaDon.ngay_nhap) == thang, KhachHang.username.like(kh) )) \
            .order_by(HoaDon.ngay_nhap).all()
        if dsNo:
            noDau.append(dsNo[0][0])
            noCuoi.append(dsNo[len(dsNo)-1][0])

    return noDau, noCuoi, tongTra, tongNo


def quy_dinh_nhap_sach():
    minNhap = QuyDinh.query.value(QuyDinh.so_luong_nhap_toi_thieu)
    maxSachTon = QuyDinh.query.value(QuyDinh.so_luong_ton_toi_thieu)
    return minNhap, maxSachTon


def chi_tiet_tien_no_KH(idKH, thang):
    tongNo = db.session.query(func.sum(ChiTietHoaDon.don_gia)) \
        .join(HoaDon, HoaDon.id == ChiTietHoaDon.id_hoadon) \
        .join(KhachHang, HoaDon.id_khachhang == KhachHang.id) \
        .filter(and_(func.month(HoaDon.ngay_nhap) == func.month(thang), KhachHang.id == idKH)).value(
        func.sum(ChiTietHoaDon.don_gia))

    return tongNo
