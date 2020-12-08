from qlnhasach import admin, db, utils
from qlnhasach.models import UserRole, Sach, PhieuNhapSach, PhieuThuTien, ChiTietPhieuNhap, KhachHang, QuyDinh
from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import UserMixin, current_user, logout_user


class NewView(ModelView):
    list_template = 'admin/model_list.html'
    create_template = 'admin/model_create.html'
    details_template = 'admin/model_details.html'
    edit_template = 'admin/model_edit.html'

    can_edit = True
    can_view_details = True
    can_create = True


class CommonView(NewView):
    def __init__(self, model, session,
                 name=None, category=None, endpoint=None, url=None, static_folder=None,
                 menu_class_name=None, menu_icon_type=None, menu_icon_value=None, user_roles=[]):
        super().__init__(model=model, session=session, name=name, category=category,
                         endpoint=endpoint, url=url, static_folder=static_folder,
                         menu_class_name=menu_class_name,
                         menu_icon_type=menu_icon_type,
                         menu_icon_value=menu_icon_value)
        self.user_roles = user_roles

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role in self.user_roles


class TraCuu(CommonView):
    column_searchable_list = ('ten_sach', 'tac_gia', 'the_loai')


# VIEW LOGOUT
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('route_logout'))

    def is_accessible(self):
        return current_user.is_authenticated


# class NhapSach(db.session):
#     idSachNhap, soLuongNhap = main.nhapsach()
#
#     minNhap = QuyDinh.query.value(QuyDinh.so_luong_nhap_toi_thieu)
#     maxSachTon = QuyDinh.query.value(QuyDinh.so_luong_ton_toi_thieu)
#     soLuongTon = db.session.query(Sach.so_luong).filter(Sach.id == idSachNhap).value(Sach.so_luong)
#     update = Sach.query.filter(Sach.id == idSachNhap).first()
#     try:
#         if soLuongNhap >= minNhap and soLuongTon < maxSachTon:
#             update.so_luong += soLuongNhap
#             db.session.commit()
#     except Exception as ex:
#         print(ex)


# VIEW CỦA ADMIN VÀ THỦ KHO
admin.add_view(CommonView(PhieuNhapSach, db.session, name="Phiếu nhập sách",
                          user_roles=[UserRole.ADMIN, UserRole.Thu_kho]))
admin.add_view(CommonView(ChiTietPhieuNhap, db.session, name="Chi tiết phiếu nhập sách",
                          user_roles=[UserRole.ADMIN, UserRole.Thu_kho]))
# admin.add_view(CommonView(Sach, db.session, name="Thêm sách mới", user_roles=[UserRole.ADMIN, UserRole.Thu_kho]))


# VIEW ADMIN VÀ THU NGÂN
admin.add_view(
    CommonView(PhieuThuTien, db.session, name="Phiếu thu tiền", user_roles=[UserRole.ADMIN, UserRole.Thu_ngan]))

# VIEW CHUNG
admin.add_view(CommonView(KhachHang, db.session, name="Danh sách khách hàng",
                          user_roles=[UserRole.ADMIN, UserRole.Thu_ngan, UserRole.Thu_kho]))
admin.add_view(TraCuu(Sach, db.session, name='Danh sách sách',
                      user_roles=[UserRole.ADMIN, UserRole.Thu_ngan, UserRole.Thu_kho]))
admin.add_view(LogoutView(name="Đăng xuất"))