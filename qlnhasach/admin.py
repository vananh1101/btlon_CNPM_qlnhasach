from qlnhasach import admin, db
from qlnhasach.models import UserRole, Sach, ChiTietPhieuNhap, PhieuNhapSach, PhieuThuTien
from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import UserMixin, current_user, logout_user, login_required


class IsAuthenticated(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


# VIEW ADMIN
class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


# # VIEW THỦ KHO
# class ThuKhoView(ModelView, AdminView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role == UserRole.Thu_kho


# VIEW KẾ TOÁN
class ThuNganView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.Thu_ngan


# VIEW THAY ĐỔI QUY ĐỊNH CỦA ADMIN
class ChangeRuleView(AdminView):
    @login_required
    @expose("/")
    def index(self):
        return self.render('admin/doiquydinh.html')


# VIEW LOGOUT
class LogoutView(IsAuthenticated):
    @login_required
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')


# VIEW LẬP BÁO CÁO CỦA KẾ TOÁN
class BaoCaoView(AdminView):
    @expose('/')
    def index(self):
        return self.render('admin/doiquydinh.html')


# VIEW TRA CỨU
# class TraCuuView(BaseView):
#     @expose("/")
#     def index(self):
#         return self.render('admin/tracuu.html')

# class KeToanAuthen(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and


# admin.add_view(ChangeRuleView(name="Thay đổi quy định"))
# # admin.add_view(AdminView(name="Tra cứu sách",))
# admin.add_view(BaoCaoView(name="Báo cáo tháng"))
# admin.add_view(ThuNganView(PhieuNhapSach, db.session))
# admin.add_view(ThuKhoView(ChiTietPhieuNhap, db.session))
# admin.add_view(LogoutView(name="Đăng xuất"))
admin.add_view(AdminView(PhieuNhapSach, db.session))
admin.add_view(AdminView(ChiTietPhieuNhap, db.session))