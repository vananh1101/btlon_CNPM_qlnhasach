from operator import and_
from sqlalchemy import func
from qlnhasach import  db
from qlnhasach.models import UserRole, Sach, PhieuNhapSach, PhieuThuTien, \
    ChiTietPhieuNhap, KhachHang, QuyDinh, HoaDon, ChiTietHoaDon


def CapNhapTienNo():
    hoaDon = db.session.query(HoaDon.id, func.sum(ChiTietHoaDon.don_gia)) \
        .join(ChiTietHoaDon, ChiTietHoaDon.id_hoadon == HoaDon.id) \
        .filter(and_( HoaDon.tinh_trang_thanh_toan == 0)).filter(
        ChiTietHoaDon.id_hoadon == HoaDon.id)

    db.session.add(hoaDon)
    db.session.commit()