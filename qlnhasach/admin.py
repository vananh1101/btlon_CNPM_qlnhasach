from operator import and_
from flask_admin.babel import gettext
import logging
from sqlalchemy import func
from qlnhasach import admin, db, utils, query
from qlnhasach.models import UserRole, Sach, PhieuNhapSach, PhieuThuTien, \
    ChiTietPhieuNhap, KhachHang, QuyDinh, HoaDon, ChiTietHoaDon
from flask import redirect, url_for, flash, request
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import current_user

log = logging.getLogger("flask-admin.sqla")


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


class CreateModel(CommonView):
    @expose('/', methods=["Post"])
    def create_model(self, form):
        try:
            model = self.build_new_instance()

            form.populate_obj(model)
            idSachNhap = form.data.get('sach').id
            soLuongNhap = form.data.get('so_luong')
            minNhap = QuyDinh.query.value(QuyDinh.so_luong_nhap_toi_thieu)
            maxSachTon = QuyDinh.query.value(QuyDinh.so_luong_ton_toi_thieu)
            soLuongTon = db.session.query(Sach.so_luong).filter(Sach.id == idSachNhap).value(Sach.so_luong)
            update = Sach.query.filter(Sach.id == idSachNhap).first()
            if soLuongNhap >= minNhap and soLuongTon < maxSachTon:
                update.so_luong += soLuongNhap
                self.session.add(model)
                self._on_model_change(form, model, True)
                self.session.commit()
            else:
                flash(gettext('Failed to create record. '), 'danger')
                self.session.rollback()
                return False
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to create record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model


class ThuTienModel(CommonView):
    @expose('/', methods=["POST"])
    def create_model(self, form):
        try:
            model = self.build_new_instance()

            form.populate_obj(model)
            idSachNhap = form.data.get('sach').id
            soLuongNhap = form.data.get('so_luong')
            minNhap = QuyDinh.query.value(QuyDinh.so_luong_nhap_toi_thieu)
            maxSachTon = QuyDinh.query.value(QuyDinh.so_luong_ton_toi_thieu)
            soLuongTon = db.session.query(Sach.so_luong).filter(Sach.id == idSachNhap).value(Sach.so_luong)
            update = Sach.query.filter(Sach.id == idSachNhap).first()
            if soLuongNhap >= minNhap and soLuongTon < maxSachTon:
                update.so_luong += soLuongNhap
                self.session.add(model)
                self._on_model_change(form, model, True)
                self.session.commit()
            else:
                flash(gettext('Failed to create record. '), 'danger')
                self.session.rollback()
                return False
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to create record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model


class DanhSachKHView(CommonView):
    can_edit = False
    can_create = False


class CreateModel(CommonView):
    @expose('/', methods=["Post"])
    def create_model(self, form):
        try:
            model = self.build_new_instance()
            minNhap, maxSachTon = utils.quy_dinh_nhap_sach()
            form.populate_obj(model)
            idSachNhap = form.data.get('sach').id
            soLuongNhap = form.data.get('so_luong')
            soLuongTon = db.session.query(Sach.so_luong).filter(Sach.id == idSachNhap).value(Sach.so_luong)
            update = Sach.query.filter(Sach.id == idSachNhap).first()
            if soLuongNhap >= minNhap and soLuongTon < maxSachTon:
                update.so_luong += soLuongNhap
                self.session.add(model)
                self._on_model_change(form, model, True)
                self.session.commit()
            else:
                flash(gettext('THÊM PHIẾU NHẬP SÁCH THẤT BẠI! (SỐ SÁCH NHẬP >= 150 VÀ LƯỢNG TỒN <300) '), 'danger')
                self.session.rollback()
                return False
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('THÊM PHIẾU NHẬP SÁCH THẤT BẠI!. %(error)s', error=str(ex)), 'error')
                log.exception('THÊM PHIẾU NHẬP SÁCH THẤT BẠI!.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model


class ThuTienModel(CommonView):
    @expose('/', methods=["POST"])
    def create_model(self, form):
        try:
            model = self.build_new_instance()

            form.populate_obj(model)
            idKH = form.data.get('khach_hang').id
            tongTienThu = float(form.data.get('tong_tien_thu'))
            ngayLapPhieu = form.data.get('ngay_thu_tien')
            suDungQD = QuyDinh.query.value(QuyDinh.tien_thu_khong_vuot_tien_no)

            if suDungQD:
                tongNo = utils.chi_tiet_tien_no_KH(idKH=idKH, thang=ngayLapPhieu)

                if tongTienThu <= tongNo:
                    self.session.add(model)
                    self._on_model_change(form, model, True)
                    self.session.commit()
                else:
                    flash(gettext('THÊM PHIẾU THU TIỀN THẤT BẠI! (SỐ TIỀN THU KHÔNG ĐƯỢC HƠN TỔNG NỢ) '), 'danger')
                    self.session.rollback()
                    return False
            else:
                self.session.add(model)
                self._on_model_change(form, model, True)
                self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('GHI THẤT BAI! MỜI KIỂM TRA LẠI. %(error)s', error=str(ex)), 'error')
                log.exception('GHI THẤT BAI! MỜI KIỂM TRA LẠI.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model


class TraCuu(CommonView):
    column_searchable_list = ('ten_sach', 'tac_gia', 'the_loai')


# VIEW LOGOUT
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('route_logout'))

    def is_accessible(self):
        return current_user.is_authenticated


class BaoCaoView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.user_role == UserRole.ADMIN
                                                  or current_user.user_role == UserRole.Thu_ngan)


class BaoCaoCongNo(BaoCaoView):
    @expose("/", methods=['POST', 'GET'])
    def index(self):
        dsKhachHang = None
        noDau = None
        noCuoi = None
        tongNo = None
        tongTra = None
        if request.method == 'POST':
            # import pdb
            # pdb.set_trace()
            dsKhachHang = utils.du_lieu_khach_hang()
            thang = int(request.form.get("month"))
            noDau, noCuoi, tongTra, tongNo = utils.du_lieu_kh_no(thang=thang)
            return self.render('admin/baocaono.html', dsKhachHang=dsKhachHang, noDau=noDau
                               , noCuoi=noCuoi, tongTra=tongTra, tongNo=tongNo)
        return self.render('admin/baocaono.html', dsKhachHang=dsKhachHang, noDau=noDau
                           , noCuoi=noCuoi, tongTra=tongTra, tongNo=tongNo)


class BaoCaoTon(BaoCaoView):
    @expose("/", methods=['POST', 'GET'])
    def index(self):
        tenSach = None
        tonDau = None
        tonCuoi = None
        tongNhap = None
        tongXuat = None
        if request.method == 'POST':
            thang = int(request.form.get("month"))
            tenSach = utils.du_lieu_sach()
            tonDau, tonCuoi, tongNhap, tongXuat = utils.du_lieu_sach_ton(thang=thang)
            return self.render('admin/baocaohangton.html', tenSach=tenSach, tonDau=tonDau, tonCuoi=tonCuoi,
                               tongNhap=tongNhap,
                               tongXuat=tongXuat)
        return self.render('admin/baocaohangton.html', tenSach=tenSach, tonDau=tonDau, tonCuoi=tonCuoi,
                           tongNhap=tongNhap,
                           tongXuat=tongXuat)


# VIEW ADMIN
admin.add_view(CommonView(QuyDinh, db.session, name='Quy định', user_roles=[UserRole.ADMIN]))

# VIEW CỦA ADMIN VÀ THỦ KHO
admin.add_view(CreateModel(PhieuNhapSach, db.session, name="Phiếu nhập sách",
                           user_roles=[UserRole.ADMIN, UserRole.Thu_kho]))
admin.add_view(CreateModel(ChiTietPhieuNhap, db.session, name="Chi tiết phiếu nhập sách",
                           user_roles=[UserRole.ADMIN, UserRole.Thu_kho]))

# VIEW ADMIN VÀ THU NGÂN
admin.add_view(ThuTienModel(PhieuThuTien, db.session, name="Phiếu thu tiền",
                            user_roles=[UserRole.ADMIN, UserRole.Thu_ngan]))
admin.add_view(CommonView(HoaDon, db.session, name="Hoá đơn", user_roles=[UserRole.ADMIN, UserRole.Thu_ngan]))
admin.add_view(CommonView(ChiTietHoaDon, db.session, name="Chi tiết hoá đơn", user_roles=[UserRole.ADMIN, UserRole.Thu_ngan]))
admin.add_view(BaoCaoTon(name='Báo cáo tồn'))
admin.add_view(BaoCaoCongNo(name='Báo cáo công nợ'))

# VIEW CHUNG
admin.add_view(DanhSachKHView(KhachHang, db.session, name="Danh sách khách hàng",
                              user_roles=[UserRole.ADMIN, UserRole.Thu_ngan, UserRole.Thu_kho]))
admin.add_view(TraCuu(Sach, db.session, name='Danh sách sách',
                      user_roles=[UserRole.ADMIN, UserRole.Thu_ngan, UserRole.Thu_kho]))
admin.add_view(LogoutView(name="Đăng xuất"))
