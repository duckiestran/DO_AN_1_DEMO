#Khởi tạo bảng
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

db = SQLAlchemy()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgre@localhost:5432/Information"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

#Thông tin đăng ký và đăng nhập của người dùng
class SignUp(db.Model): 
    __tablename___ = "SignUp"
    number_phone = db.Column(db.Integer, primary_key=True) #số điện thoại đăng ký
    password = db.Column(db.String, nullable=False) #Mật khẩu
    name = db.Column(db.String, nullable=False) #Tên người dùng
    birth = db.Column(db.DATE, nullable=False) #Năm sinh người dùng



#Thông tin của nhà trọ cho thuê
class Hostel(db.Model):
    __tablename__ = "Hostel"
    key_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False) #Mô tả trọ
    price = db.Column(db.String, nullable=False) #Tiền thuê nhà
    acreage = db.Column(db.String, nullable=False) #Diện tích nhà
    location = db.Column(db.String, nullable=False) #Địa chỉ nhà



#Thông tin của Admin
class Admin(db.Model):
    __tablename__ = "Admin"
    phone_admin = db.Column(db.Integer, primary_key=True) #Số điện thoại Admin
    pass_admin = db.Column(db.String, nullable=False) #Mẩt khẩu