from qlnhasach import admin
from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import UserMixin, current_user, logout_user


# VIEW ADMIN
class BaseAdmin(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class ChangeRuleView(BaseAdmin):
    @expose("/")
    def index(self):
        return self.render('admin/doiquydinh.html')


class LogoutView(BaseAdmin):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class ReportView(BaseAdmin):
    @expose('/')
    def index(self):
        return self.render('admin/report.html')

class SearchView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/tracuu.html')


admin.add_view(ChangeRuleView(name="Thay đổi quy định"))
admin.add_view(SearchView(name="Tra cứu sách"))
admin.add_view(ReportView(name='Báo cáo tháng'))
admin.add_view(LogoutView(name="Đăng xuất"))
