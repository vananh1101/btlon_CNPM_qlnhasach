from qlnhasach.models import Sach
from qlnhasach import db


def read_data():
    dssach = Sach.query
    return dssach.all()
