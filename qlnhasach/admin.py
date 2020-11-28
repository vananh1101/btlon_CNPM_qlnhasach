from qlnhasach import admin
from qlnhasach.models import UserRole
from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import UserMixin, current_user, logout_user


class IsAuthenticated(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


# VIEW ADMIN
class AdminView(IsAuthenticated):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


# VIEW THỦ KHO
class ThuKhoView(IsAuthenticated):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.Thu_kho


# VIEW KẾ TOÁN
class ThuNganView(IsAuthenticated):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.Thu_ngan


# VIEW LẬP PHIẾU NHẬP SÁCH CỦA THỦ KHO
class NhapSachView(AdminView, ThuKhoView):
    @expose("/")
    def index(self):
        return self.render("admin/phieunhapsach.html")


# VIEW THAY ĐỔI QUY ĐỊNH CỦA ADMIN
class ChangeRuleView(AdminView):
    @expose("/")
    def index(self):
        return self.render('admin/doiquydinh.html')


# VIEW LOGOUT
class LogoutView(IsAuthenticated):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


# VIEW LẬP BÁO CÁO CỦA KẾ TOÁN
class BaoCaoView(AdminView, ThuNganView):
    @expose('/')
    def index(self):
        return self.render('admin/report.html')


# VIEW TRA CỨU
class TraCuuView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/tracuu.html')


admin.add_view(ChangeRuleView(name="Thay đổi quy định"))
admin.add_view(TraCuuView(name="Tra cứu sách"))
admin.add_view(BaoCaoView(name="Báo cáo tháng"))
admin.add_view(NhapSachView(name="Phieu nhap sach"))
admin.add_view(LogoutView(name="Đăng xuất"))
