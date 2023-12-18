from server2 import *

from flask import Flask, request, render_template,url_for,redirect,request

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.exc import DataError

from sqlalchemy import Integer, cast



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgre@localhost:5432/Information"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


#____________________________________

#Admin /Xong
@app.route("/admin") 
def admin():
    return render_template("admin.html")

@app.route("/admin2") 
def admin2():
    return render_template("control.html")

#trang đăng nhập / Xong
@app.route("/timtro365") 
def home():
    return render_template("index.html")
 
#trang đăng ký /Xong
@app.route("/signup")
def signup():
    return render_template("signup.html")

#thông báo đăng ký tài khoản thành công /Xong
@app.route("/success")
def timtro():
    return render_template("success.html")

#tìm kiếm nhà trọ theo khu vực người dùng chọn /Xong
@app.route('/search')  
def search():
    hostel = Hostel.query.all()
    return render_template("search.html", Hostel=hostel)


#trang chủ web /Xong
@app.route("/homepage")
def homepage():
    return render_template("home.html")

#thông tin tài khoản
@app.route("/profile")
def profile():
    return render_template("profile.html")


#test
@app.route("/test")
def test():
    return render_template("test.html")




#______________________________________
#Tài khoản admin
@app.route("/login_ad", methods=["GET","POST"]) #GET là yêu cầu dữ liệu từ bên sever thông qua URL của web/POST là gửi dữ liệu từ client lên sever  
                                              
def login_ad():
    try:
        if request.method == "POST":
            phone_admin = request.form.get("phone_admin")
            pass_admin = request.form.get("pass_admin")
            
        
            ad = Admin.query.filter_by(phone_admin=phone_admin).first() #check tài khoản mật khẩu trong database
            if ad and ad.pass_admin == pass_admin:
                return redirect(url_for("admin2")) #đăng nhập thành công thì return về trang chủ
            else:
                return render_template("admin.html")
        else:
            return render_template("admin.html")
        
    except DataError:
        return redirect(url_for("admin")) #nhập chữ vào số điện thoại sẽ return về lại trang đăng nhập

#______________________________________
#Thông tin đăng ký mới 
@app.route("/Signup")  
def Signup():   
    number_phone = request.args.get("phone")
    password = request.args.get("password")#request về password bên signup
    name = request.args.get("name")
    birth = request.args.get("birth")
        
        
    name_signup = SignUp(number_phone=number_phone, password=password,name=name,birth=birth) #pass ở đầu là var bên Create_tableSQL, pass còn lại là var bên này
    db.session.add(name_signup)  
    db.session.commit()

    return render_template("success.html")

#_________________________________________
#Đăng nhập vào web
#check tài khoản mật khẩu để đăng nhập
@app.route("/login", methods=["GET","POST"]) #GET là yêu cầu dữ liệu từ bên sever thông qua URL của web/POST là gửi dữ liệu từ client lên sever  
                                              
def login():
    try:
        if request.method == "POST":
            number_phone = request.form.get("phone")
            password = request.form.get("password")
        
            user = SignUp.query.filter_by(number_phone=number_phone).first() #check tài khoản mật khẩu trong database
            if user and user.password == password:
                return redirect(url_for("homepage")) #đăng nhập thành công thì return về trang chủ
            else:
                return render_template("index.html")
        else:
            return render_template("index.html")
        
    except DataError:
        return redirect(url_for("timtro365")) #nhập chữ vào số điện thoại sẽ return về lại trang đăng nhập


#_________________________________________
#Tìm kiếm nhà trọ theo khu vực
@app.route("/result", methods=["get"])
def result():

    # Nhận thông tin từ form bên search.html
    location = request.args.get("location")
    price_range = request.args.get("price")
    acreage_range = request.args.get("acreage")

    # Xử lý truy vấn
    query = Hostel.query

    #khu vực
    if location:
        search_location = f"%{location}%"
        query = query.filter(Hostel.location.like(search_location))
    
    #Giá cả
    if price_range:
        price_range = price_range.replace(",", "").strip()
            
        if "-" in price_range:
            min_price, max_price = map(str, price_range.split("-"))
            query = query.filter(cast(Hostel.price, Integer).between(min_price, max_price))
        else:
            min_price, max_price = 0, 0 # Xử lý khi không có dấu "-"
    
    query = query.filter(cast(Hostel.price, Integer).between(min_price, max_price)) # Sử dụng cast để chuyển đổi kiểu dữ liệu của cột
    
    #Diện tích
    if acreage_range:
        acreage_range = acreage_range.replace(",", "").strip()
        
        if "-" in acreage_range:
            min_acreage, max_acreage = map(str, acreage_range.split("-"))
            query = query.filter(cast(Hostel.acreage, Integer).between(min_acreage, max_acreage))
        else:    
            min_acreage, max_acreage = 0, 0

    query = query.filter(cast(Hostel.acreage, Integer).between(min_acreage, max_acreage))
    

   # Thực hiện truy vấn
    result_hostels = query.all()
    return render_template("result.html", hostels=result_hostels)

#_____________________________________________
#Phân quyền

#Thêm bài viết (?) Cái này k phải phân quyền
@app.route("/addPostSuccess")
def addPostSuccess():
    key_id = request.args.get("key_id")
    title = request.args.get("title")
    price = request.args.get("price")
    acreage = request.args.get("acreage")
    location = request.args.get("location")
    # Request ra id, tiêu đề, giá cả, diện tích, vị trí khi thêm 1 bài viết
    room = Hostel(title=title, price=price, acreage=acreage, location=location, key_id=key_id)
    db.session.add(room)
    db.session.commit()
    return render_template("add-posts-success.html")

#show ra các thông tin trọ
@app.route("/showPostsForRent")
def showPostsForRent():
    result_hostels = Hostel.query.all()
    return render_template("show-all-posts.html", hostels=result_hostels)

#Xóa bài đăng
@app.route("/delPosts")
def delPosts():
    return render_template("del-posts.html")

#Thông báo xóa bài đăng thành công
@app.route("/delPostsSuccess")
def delPostsSuccess():
    key_id = request.args.get("key_id")
    exists = False
    exists = Hostel.query.filter_by(key_id=key_id)
    while exists:
        obj = Hostel.query.filter_by(key_id=key_id).first()
        db.session.delete(obj)
        db.session.commit()
        return render_template("del-Posts-success.html")
    else:
        return render_template("invalidkey_id.html")

# Quản lý người dùng-Chỉ dùng cho Admin 
@app.route("/userManagement")
def userManagement():
    users = SignUp.query.all()
    return render_template("user-management.html", users=users)


# Xoá người dùng-Chỉ dùng cho Admin
def delUser():
    return render_template("del-users.html")

# Thông báo xoá bài đăng
@app.route("/delUserSuccess")
def delUserSuccess():
    number_phone = request.args.get("number_phone")
    exists = False
    exists = SignUp.query.filter_by(number_phone=number_phone)
    while exists:
        user = SignUp.query.filter_by(number_phone=number_phone).first()
        db.session.delete(user)
        db.session.commit()
        return render_template("del-users-success.html")
    else:
        return render_template("invalidkey_id.html")





