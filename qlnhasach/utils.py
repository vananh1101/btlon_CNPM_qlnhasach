from qlnhasach.models import Sach, QuyDinh
from flask import request
from qlnhasach import db


def read_data():
    dssach = Sach.query
    return dssach.all()


