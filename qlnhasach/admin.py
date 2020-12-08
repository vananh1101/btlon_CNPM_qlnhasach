from qlnhasach import admin, db,app
from qlnhasach.models import UserRole, Sach, PhieuNhapSach, PhieuThuTien, ChiTietPhieuNhap
from flask import redirect, url_for, render_template
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import UserMixin, current_user, logout_user


# VIEW ADMIN
class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


# # VIEW THỦ KHO
# class ThuKhoView(ModelView):
#
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role == UserRole.Thu_kho
#
#
# # VIEW KẾ TOÁN
# class ThuNganView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role == UserRole.Thu_ngan


class CommonView(ModelView):
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


# VIEW THAY ĐỔI QUY ĐỊNH CỦA ADMIN
class ChangeRuleView(AdminView):
    @expose("/")
    def index(self):
        return self.render('admin/doiquydinh.html')


# VIEW LOGOUT
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')

    def is_accessible(self):
        return current_user.is_authenticated


# VIEW LẬP BÁO CÁO CỦA KẾ TOÁN
class BaoCaoView(AdminView):
    @expose('/')
    def index(self):
        return self.render('admin/doiquydinh.html')


# admin.add_view(ChangeRuleView(name="Thay đổi quy định"))
# admin.add_view(CommonView(BaoCaoView, db.session, name="Báo cáo",
#                           user_roles=[UserRole.ADMIN, UserRole.Thu_ngan]))
admin.add_view(CommonView(PhieuNhapSach, db.session, name="Phiếu nhập sách",
                          user_roles=[UserRole.ADMIN, UserRole.Thu_kho]))
admin.add_view(CommonView(ChiTietPhieuNhap, db.session, name="Chi tiết phiếu nhập sách",
                          user_roles=[UserRole.ADMIN, UserRole.Thu_kho]))
admin.add_view(ModelView(Sach, db.session))
admin.add_view(LogoutView(name="Đăng xuất"))