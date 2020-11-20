from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Float, Column, Enum, Date, Boolean
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime
from qlnhasach import db


class QLBase(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class UserRole(UserEnum):
    ADMIN = 1
    Thu_kho = 2
    Thu_ngan = 3


class User(QLBase, UserMixin):
    __tablename__ = 'user'

    email = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    avatar = Column(String(100))
    joined_date = Column(Date, default=datetime.now())
    user_role = Column(Enum(UserRole), nullable=False)


if __name__ == "__main__":
    db.create_all()
